package org.limine.entry.tool.processes;

import org.limine.entry.tool.formats.limine8.Limine;
import org.limine.entry.tool.objects.Config;
import org.limine.entry.tool.objects.Output;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import static org.limine.entry.tool.processes.Utility.*;


public class ConfigReader {

    private final Map<String, String> configs = new HashMap<>();
    private final Map<String, String> kernelCmdlineMap = new HashMap<>();

    public ConfigReader() {
        // Load configs in order: lowest to highest priority
        loadConfigDir("/usr/share/limine-entry-tool.d"); // 1. Lowest priority
        loadConfigFile("/etc/limine-entry-tool.conf");   // 2.
        loadConfigDir("/etc/limine-entry-tool.d");       // 3.
        loadConfigFile(Config.DEFAULT_CONFIG_FILE_PATH); // 4. Highest priority

        boolean quiet = "yes".equalsIgnoreCase(configs.get("QUIET_MODE"));
        Config.QUIET = Config.QUIET || quiet;
        detectColorSupport();
    }

    public static void detectColorSupport() {
        Output c = Utility.getCommandOutput("tput colors", false, false);
        if (c.isSuccess() && !c.text().isEmpty()) {
            try {
                Config.ENABLE_COLOR = Integer.parseInt(c.text().getFirst().trim()) >= 8;
            } catch (NumberFormatException ignored) {
                Config.ENABLE_COLOR = false;
            }
        }
        Config.ENABLE_UNICODE = Utility.isUnicodeSupported();
    }

    private void loadConfigDir(String dirPath) {
        Path dir = Paths.get(dirPath);
        if (!Files.isDirectory(dir)) return;

        try (Stream<Path> stream = Files.list(dir)) {
            stream.filter(p -> p.getFileName().toString().endsWith(".conf") && Files.isRegularFile(p))
                    .sorted(Comparator.comparing(Path::getFileName))
                    .forEach(p -> loadConfigFile(p.toString()));
        } catch (IOException e) {
            exitWithError("Failed to load config directory:", dirPath + " due to " + e.getMessage());
        }
    }

    private void loadConfigFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) return;

        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();

                // Skip empty lines and comments
                if (line.isEmpty() || line.startsWith("#")) continue;

                String key;
                String value;
                boolean append = false;

                int appendIndex = line.indexOf("+=");
                int eqIndex = line.indexOf('=');

                if (appendIndex != -1) {
                    key = line.substring(0, appendIndex).trim();
                    value = removeSurrounding(line.substring(appendIndex + 2).trim(), "\"");
                    append = true;
                } else if (eqIndex != -1) {
                    key = line.substring(0, eqIndex).trim();
                    value = removeSurrounding(line.substring(eqIndex + 1).trim(), "\"");
                } else {
                    continue; // Invalid line
                }

                if (!parseKernelCmdline(key, value, append)) {
                    configs.put(key, value);
                }
            }
        } catch (IOException e) {
            exitWithError("Failed to load config file:", filePath + " due to " + e.getMessage());
        }
    }

    private boolean parseKernelCmdline(String key, String value, boolean append) {
        final String prefix = "KERNEL_CMDLINE";

        if (!key.startsWith(prefix)) {
            return false;
        }

        String targetKey = "default";

        if (key.length() > prefix.length() && key.charAt(prefix.length()) == '[') {
            int start = prefix.length() + 1;
            int end = key.indexOf(']', start);

            if (start > end) {
                return false;
            }

            String extractedKey = key.substring(start, end).trim();
            extractedKey = removeSurrounding(extractedKey, "\"");
            if (!extractedKey.isEmpty()) {
                targetKey = extractedKey;
            }
        } else if (key.length() != prefix.length()) {
            return false; // Invalid format
        }

        if (append && kernelCmdlineMap.containsKey(targetKey)) {
            kernelCmdlineMap.compute(targetKey, (k, existing) -> value + " " + existing);
        } else {
            kernelCmdlineMap.put(targetKey, value);
        }

        return true;
    }

    public Config readConfig() {
        String targetOs = configs.get("TARGET_OS_NAME");
        if (targetOs == null || targetOs.isBlank()) {
            targetOs = getLinuxDistroName();
        } else {
            targetOs = Limine.cleanName(targetOs);
        }

        String espPath = configs.get("ESP_PATH");
        if (espPath == null || espPath.isBlank()) {
            espPath = Utility.findBootPartition();
            if (espPath == null) {
                exitWithError("FAT32 boot partition not found. Make sure it is mounted or configure ESP_PATH in " + Config.DEFAULT_CONFIG_FILE_PATH);
                return null;
            }
        } else if (!validateVfatPartition(espPath)) {
            exitWithError("\"" + espPath + "\" is not a valid FAT32 boot partition. Please correct ESP_PATH in " + Config.DEFAULT_CONFIG_FILE_PATH);
            return null;
        }

        String spaceNumber = configs.get("SPACE_NUMBER");
        if (spaceNumber != null) {
            try {
                int number = Integer.parseInt(spaceNumber);
                StringBuilder spaces = new StringBuilder();
                while (number > 0) {
                    spaces.append(" ");
                    number--;
                }
                Config.SPACES = spaces.toString();
            } catch (NumberFormatException ignored) {
                errorMessage("Value of SPACE_NUMBER should be a number and not a word!");
            }
        }

        String enableVerification = configs.get("ENABLE_VERIFICATION");
        if (enableVerification != null) {
            Config.ENABLE_VERIFICATION = Utility.isCommandPresent(Config.HASH_COMMAND) && "yes".equalsIgnoreCase(enableVerification);
        } else {
            Config.ENABLE_VERIFICATION = false;
        }

        String configBackupThreshold = configs.get("CONFIG_BACKUP_THRESHOLD");
        if (configBackupThreshold != null) {
            try {
                Config.CONFIG_BACKUP_THRESHOLD = Integer.parseInt(configBackupThreshold);
            } catch (NumberFormatException e) {
                errorMessage("CONFIG_BACKUP_THRESHOLD=" + configBackupThreshold + " is invalid, it should be in hours format.");
            }
        }

        String bootOrder = configs.get("BOOT_ORDER");
        if (bootOrder != null) {
            if (!bootOrder.isBlank()) {
                Config.BOOT_ORDER = Arrays.stream(bootOrder.split(",")).map(String::trim).toArray(String[]::new);
            }
        }

        String enableSort = configs.get("ENABLE_SORT");
        if (enableSort != null) {
            if ("yes".equalsIgnoreCase(enableSort)) {
                Config.ENABLE_SORT = true;
            }
        }

        String machineID = readMachineID();

        String customUkiName = configs.get("CUSTOM_UKI_NAME");
        Pattern validName = Pattern.compile("^[a-z0-9]+$");
        if (customUkiName != null && !customUkiName.isBlank() && validName.matcher(customUkiName).matches()) {
            Config.UKI_FILE_PREFIX = customUkiName;
        } else {
            Config.UKI_FILE_PREFIX = machineID;
        }

        return new Config(machineID, targetOs, espPath, Limine.DEFAULT_PATH_FUNCTION.toString());
    }

    public Map<String, String> readBootOptions() {
        String defaultCmdline = kernelCmdlineMap.get("default");
        if (defaultCmdline == null || defaultCmdline.isBlank()) {
            kernelCmdlineMap.put("default", readKernelCmdline());
        }
        return kernelCmdlineMap;
    }
}
