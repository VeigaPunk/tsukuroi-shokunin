package org.limine.entry.tool.processes;

import org.limine.entry.tool.objects.Config;
import org.limine.entry.tool.objects.ConsoleColor;
import org.limine.entry.tool.objects.LogLevel;
import org.limine.entry.tool.objects.Output;

import java.io.*;
import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermission;
import java.nio.file.attribute.PosixFilePermissions;
import java.security.SecureRandom;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Utility {

    private static final int MACHINE_ID_LENGTH = 32;
    private static final String MACHINE_ID_FILE_PATH = "/etc/machine-id";

    public static void ensureDirectoryExists(String dirPath) {
        // Construct the full directory path
        File dir = new File(dirPath);
        // Check if the directory exists
        if (!dir.exists()) {
            // If it doesn't exist, create the directory
            if (!dir.mkdirs()) {
                errorMessage("Failed to create directory:", dir.getPath());
            }
        }
    }

    /**
     * Generate a machine ID in /etc/machine-id
     */
    public static String readMachineID() {
        String machineID;
        try {
            machineID = new String(Files.readAllBytes(Paths.get("/etc/machine-id"))).trim();
        } catch (IOException e) {
            machineID = generateRandomMachineID();
        }
        if (machineID.length() != 32) {
            exitWithError("Invalid machine-ID length: " + machineID.length() + ". The length should be 32");
        }
        return machineID;
    }

    public static boolean isFilePresent(String filePath) {
        File file = new File(filePath);
        return file.exists() && file.isFile();
    }

    public static boolean isDirectoryPresent(String dirPath) {
        Path path = Paths.get(dirPath);
        try {
            // Check if the path exists and is a directory (following symbolic links)
            return Files.exists(path) && Files.isDirectory(path);
        } catch (Exception e) {
            return false;
        }
    }

    public static boolean isUnicodeSupported() {
        String locale = System.getenv("LC_ALL");
        if (locale == null || locale.isEmpty()) {
            locale = System.getenv("LANG");
        }
        return locale != null && locale.toUpperCase().contains("UTF-8");
    }

    public static String generateRandomMachineID() {
        SecureRandom random = new SecureRandom();
        StringBuilder newMachineID = new StringBuilder(MACHINE_ID_LENGTH);
        for (int i = 0; i < MACHINE_ID_LENGTH; i++) {
            int nextInt = random.nextInt(16); // 0-15 for hexadecimal
            newMachineID.append(Integer.toHexString(nextInt));
        }
        try {
            Files.writeString(Paths.get(MACHINE_ID_FILE_PATH), newMachineID);
            infoMessage("New machine-id generated:", String.valueOf(newMachineID));
            infoMessage("This machine-id saved:", MACHINE_ID_FILE_PATH);
            changeFilePermissions(MACHINE_ID_FILE_PATH, "r--r--r--");
        } catch (IOException e) {
            exitWithError("New machine ID generator failed. Error:", e.getMessage());
        }
        return newMachineID.toString();
    }

    public static void changeFilePermissions(String filePath, String permissions) {
        Path path = Paths.get(filePath);
        // Convert the permission string to a set of PosixFilePermissions
        Set<PosixFilePermission> perms = PosixFilePermissions.fromString(permissions);
        try {
            Files.setPosixFilePermissions(path, perms);
            infoMessage("Permissions " + permissions + " changed for file:", filePath);
        } catch (IOException e) {
            errorMessage("Failed to change permissions " + permissions + " for file: ", filePath);
        }
    }

    private static String extractHash(String outputLine) {
        StringBuilder hash = new StringBuilder();
        outputLine = outputLine.trim();
        for (int i = 0; i < outputLine.length(); i++) {
            char c = outputLine.charAt(i);
            if (c == ' ') {
                break;
            }
            hash.append(c);
        }
        return hash.toString();
    }

    public static String computeBlake2(String absoluteFilePath) {
        return blake2IntegrityCheck(absoluteFilePath, 2);
    }

    private static String blake2sum(String absoluteFilePath) {
        Output output = Utility.getCommandOutput(Config.HASH_COMMAND + " " + absoluteFilePath, false, true);
        if (output.isSuccess()) {
            return Utility.extractHash(output.text().getFirst());
        } else {
            return "";
        }
    }

    /**
     * Calculate the hash of a file using two parallel threads and check for hash corruption.
     * If corruption is detected, the process is repeated a specified number of times.
     *
     * @param absoluteFilePath  The path of the file to calculate the hash for.
     * @param repeatIfCorrupted The number of times to retry if corruption is detected.
     * @return The final hash if no corruption is detected.
     */
    public static String blake2IntegrityCheck(String absoluteFilePath, int repeatIfCorrupted) {
        int attempts = 0;
        while (attempts <= repeatIfCorrupted) {
            try {
                // Run hash calculation asynchronously in two threads using CompletableFuture
                CompletableFuture<String> hashFuture1 = CompletableFuture.supplyAsync(() -> blake2sum(absoluteFilePath));
                CompletableFuture<String> hashFuture2 = CompletableFuture.supplyAsync(() -> blake2sum(absoluteFilePath));

                // Get the hash results from both futures
                String hashResult1 = hashFuture1.get();
                String hashResult2 = hashFuture2.get();

                // Compare the results
                if (hashResult1.equals(hashResult2)) {
                    return hashResult1;  // Return the hash if they match (no corruption detected)
                } else {
                    // Log and print an error message if corruption is detected
                    String errMessage = String.format(
                            "Hardware (RAM/CPU) error detected! Hash mismatch for file: %s (attempt %d/%d).",
                            absoluteFilePath, attempts + 1, repeatIfCorrupted + 1
                    );
                    errorMessage(errMessage);

                    if (attempts == repeatIfCorrupted) {
                        // If max attempts reached, return the first result and log a critical error
                        errorMessage("Repeated hash mismatches. Hardware is faulty. Returning corrupted hash for file:" + absoluteFilePath);
                        return hashResult1;
                    }
                }
            } catch (InterruptedException | ExecutionException e) {
                throw new RuntimeException("Error occurred while calculating the hash.", e);
            }
            attempts++;
        }
        // Should not reach this point, but return the last result as a fallback
        throw new IllegalStateException("Unexpected state in hash calculation.");
    }

    public static void copyFile(String sourceFilePath, String targetFilePath, boolean force, boolean showOutput) {
        if (sourceFilePath == null || sourceFilePath.isBlank()) {
            return;
        }
        Path source = Path.of(sourceFilePath);
        Path target = Path.of(targetFilePath);
        try {
            if (force) {
                Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
            } else {
                Files.copy(source, target);
            }
            if (showOutput) {
                infoMessage("Copied:", sourceFilePath + " -> " + targetFilePath);
            }
        } catch (IOException e) {
            errorMessage("Failed to copy:", sourceFilePath + " -> " + targetFilePath + " (" + e.getMessage() + ")");
        }
    }

    public static void copyFile(String sourceFilePath, String targetFilePath) {
        copyFile(sourceFilePath, targetFilePath, true, true);
    }

    public static void copyFileIfMissingOrDifferent(String sourceFilePath, String targetFilePath) {
        if (!isFilePresent(sourceFilePath) || Objects.equals(sourceFilePath, targetFilePath)) {
            return;
        }
        if (!isCommandPresent(Config.HASH_COMMAND)) {
            copyFile(sourceFilePath, targetFilePath);
            return;
        }

        if (isFilePresent(targetFilePath)) {
            var sourceHashCode = computeBlake2(sourceFilePath);
            var targetHashCode = computeBlake2(targetFilePath);
            if (!sourceHashCode.equals(targetHashCode)) {
                copyFile(sourceFilePath, targetFilePath);
            }
        } else {
            copyFile(sourceFilePath, targetFilePath);
        }
    }

    public static void moveFile(String sourceFilePath, String targetFilePath, boolean force, boolean showOutput) {
        if (sourceFilePath == null || sourceFilePath.isBlank()) {
            return;
        }
        Path source = Path.of(sourceFilePath);
        Path target = Path.of(targetFilePath);
        try {
            if (force) {
                Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);
            } else {
                Files.move(source, target);
            }
            if (showOutput) {
                infoMessage("Moved:", sourceFilePath + " -> " + targetFilePath);
            }
        } catch (IOException e) {
            errorMessage("Failed to move:", sourceFilePath + " -> " + targetFilePath + " (" + e.getMessage() + ")");
        }
    }

    public static void deleteDirectory(String dirPath) {
        if (dirPath == null || dirPath.isBlank() || "/".equals(dirPath.trim()) || dirPath.trim().startsWith("/home")) {
            return;
        }
        if (isDirectoryPresent(dirPath)) {
            if (Utility.runCommand("rm -r '" + dirPath + "'", true, false)) {
                infoMessage("Deleted:", dirPath);
            } else {
                errorMessage("Failed to delete:", dirPath);
            }
        }
    }

    public static void deleteFile(String absoluteFilePath, boolean showOutput) {
        if (absoluteFilePath == null || absoluteFilePath.isBlank()) {
            return;
        }
        Path path = Path.of(absoluteFilePath);
        try {
            if (Files.deleteIfExists(path)) {
                if (showOutput) {
                    infoMessage("Removed:", absoluteFilePath);
                }
            }
        } catch (IOException e) {
            errorMessage("Failed to remove:", absoluteFilePath + " (" + e.getMessage() + ")");
        }
    }

    public static void deleteFile(String absoluteFilePath) {
        deleteFile(absoluteFilePath, true);
    }

    /**
     * Get the result from a command output using ProcessBuilder.
     *
     * @param commandLine         The command to be executed.
     * @param exitIfError         If true, the application will exit in case of error.
     * @param displayErrorMessage Error message to display/log in case of error.
     * @return List of strings containing the output of the command.
     */
    public static Output getCommandOutput(String commandLine, boolean exitIfError, boolean displayErrorMessage) {
        // Use ProcessBuilder to create and start the process
        ProcessBuilder processBuilder = new ProcessBuilder("bash", "-c", commandLine)
                .redirectErrorStream(true);// Redirect error stream to the standard output stream
        try {
            Process process = processBuilder.start();
            List<String> textOutput = new ArrayList<>();

            // Use try-with-resources to automatically close BufferedReader
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                reader.lines().forEach(textOutput::add);
            }

            // Wait for the process to finish and get the exit code
            int errorCode = process.waitFor();
            if (errorCode == 0) {
                return new Output(textOutput, null, errorCode, true);
            }
            if (displayErrorMessage) {
                errorMessage("Command failed:", commandLine);
                if (!textOutput.isEmpty()) {
                    if (!textOutput.getFirst().trim().isEmpty()) {
                        errorMessage("Output:", Arrays.toString(textOutput.toArray()));
                    }
                }
            }
            if (exitIfError) {
                exitWithError("Exit code:", String.valueOf(errorCode));
            }
            return new Output(null, textOutput, errorCode, false);
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }


    /**
     * Run multiple commands.
     */
    public static boolean runCommands(List<String> commands, boolean stopNextCommandOnError, boolean showOutput, boolean showCommand) {
        boolean isSuccess = true;
        try {
            for (String command : commands) {
                ProcessBuilder processBuilder = new ProcessBuilder("bash", "-c", command).redirectErrorStream(true);
                Process process = processBuilder.start();
                CompletableFuture<Void> outputFuture = null;
                if (showOutput) {
                    // Use CompletableFuture to asynchronously read output and error streams
                    outputFuture = CompletableFuture.runAsync(() -> printStream(process.getInputStream()));
                }
                // Wait for the process to complete
                int errorCode = process.waitFor();
                if (showOutput) {
                    // Wait for the output/error streams to finish processing
                    outputFuture.join();
                }
                if (errorCode != 0) {
                    isSuccess = false;
                    errorMessage("Command failed:", "\"" + command + "\" with exit code: " + errorCode);
                    if (stopNextCommandOnError) {
                        // Stop continues to the next command
                        break;
                    }
                } else {
                    if (showCommand) {
                        infoMessage("Command:", command);
                    }
                }
            }
            return isSuccess;
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private static void printStream(InputStream inputStream) {
        try {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = inputStream.read(buffer)) != -1) {
                String text = new String(buffer, 0, len);
                System.out.print(text);
            }
        } catch (IOException ignored) {
        }
    }


    public static boolean runCommand(String command, boolean showOutput, boolean showCommand) {
        return runCommands(List.of(command), true, showOutput, showCommand);
    }


    public static String extractFileNameFromPath(String path) {
        int lastIndex = path.lastIndexOf('/');
        if (lastIndex != -1) {
            return path.substring(lastIndex + 1);
        } else {
            // If no '/' is found, return the entire path as a file name
            return path;
        }
    }


    /**
     * Logger
     */
    public static void loggerSend(String message, LogLevel logLevel) {
        try {
            // Bugfix: Do not use Runtime.getRuntime() that has a bug to escape some character like '-'
            // Use ProcessBuilder instead.
            Process process = new ProcessBuilder("bash", "-c", "logger -t limine-entry-tool -p " + logLevel.level + " \"" + message + "\"").start();
            process.waitFor();
        } catch (IOException | InterruptedException ignored) {
        }
    }


    /**
     * Returns a string representing the device and inode of the given path.
     * This is used to detect chroot environments by comparing the root (/)
     * of the current process with the root of PID 1 (/proc/1/root/.).
     *
     * @param path The filesystem path to check (e.g., "/", "/proc/1/root/.")
     * @return A string in the format "device:inode" if successful, or null if an error occurs.
     */
    public static String getDeviceAndInode(String path) {
        try {
            Path p = Paths.get(path);
            Object devAttr = Files.getAttribute(p, "unix:dev");
            Object inoAttr = Files.getAttribute(p, "unix:ino");

            if (devAttr instanceof Long && inoAttr instanceof Long) {
                return devAttr + ":" + inoAttr;
            }
            return null;
        } catch (IOException ignored) {
            return null; // path cannot be accessed or attributes cannot be read
        }
    }


    /**
     * Reads the kernel command line options.
     * Logic:
     * 1. Prefer /etc/kernel/cmdline
     * 2. If missing, read /proc/cmdline, but only if not running in a chroot.
     * 3. If running in a chroot and /etc/kernel/cmdline is missing, warn users.
     *
     * @return Kernel command line as a string with trailing line breaks removed, or empty string if unavailable.
     */
    public static String readKernelCmdline() {
        Path etcCmdline = Paths.get("/etc/kernel/cmdline");
        if (Files.exists(etcCmdline)) {
            try {
                String content = Files.readString(etcCmdline);
                content = content.replace("\n", " ").trim();
                if (!content.isBlank()) {
                    return content;
                }
                // if empty, continue to /proc/cmdline
            } catch (IOException ignored) {
                // Fall through to next step
            }
        }

        // Chroot detection by comparing device and inode of / vs /proc/1/root/.
        String root = getDeviceAndInode("/");
        String pid1Root = getDeviceAndInode("/proc/1/root/.");
        if (root != null && pid1Root != null && !root.equals(pid1Root)) {
            warnMessage("Detected a chroot environment, skipping reading /proc/cmdline");
            exitWithError("Kernel command line is not available. Please create and configure /etc/kernel/cmdline");
        }

        Path procCmdline = Paths.get("/proc/cmdline");
        if (Files.exists(procCmdline)) {
            try {
                String content = Files.readString(procCmdline);
                return content.replace("\n", " ").trim();
            } catch (IOException ignored) {
                return "";
            }
        }

        return "";
    }


    public static String getLinuxDistroName() {
        Path osReleasePath = Paths.get("/etc/os-release");
        try {
            if (Files.exists(osReleasePath)) {
                List<String> lines = Files.readAllLines(osReleasePath);

                for (String line : lines) {
                    if (line.startsWith("PRETTY_NAME=")) {
                        return line.split("=")[1].replace("\"", "");
                    }
                }
                for (String line : lines) {
                    if (line.startsWith("NAME=")) {
                        return line.split("=")[1].replace("\"", "");
                    }
                }
            }

            Path debianVersionPath = Paths.get("/etc/debian_version");
            Path redhatVersionPath = Paths.get("/etc/redhat-release");

            // Fallbacks if /etc/os-release is not available
            if (Files.exists(Paths.get("/etc/lsb-release"))) {
                return getLinuxDistroNameFromLsbReleaseFile();

            } else if (Files.exists(debianVersionPath)) {
                return "Debian " + Files.readString(debianVersionPath).trim();

            } else if (Files.exists(redhatVersionPath)) {
                return Files.readString(redhatVersionPath).trim();

            }
        } catch (IOException e) {
            errorMessage("Error reading Linux Distro information:", e.getMessage());
        }
        return null; // Return null if no information is found
    }

    private static String getLinuxDistroNameFromLsbReleaseFile() throws IOException {
        List<String> lines = Files.readAllLines(Paths.get("/etc/lsb-release"));
        for (String line : lines) {
            if (line.startsWith("DISTRIB_DESCRIPTION=")) {
                return line.split("=")[1].replace("\"", "").trim();
            }
        }
        return null;
    }


    public static String buildPath(String... parts) {
        String path = Paths.get("", parts).toString();
        if (path.startsWith(File.separator)) {
            return path;
        } else {
            return File.separator + path;
        }
    }


    /**
     * Check whether the command exists.
     */
    public static boolean isCommandPresent(String command) {
        // Get the PATH environment variable
        String pathEnv = System.getenv("PATH");
        if (pathEnv == null || pathEnv.isEmpty()) {
            return false; // If the PATH is empty, the command cannot be found
        }

        // Split the PATH by the system's path separator (":" on Linux/Unix)
        String[] paths = pathEnv.split(File.pathSeparator);

        // Iterate through each directory in PATH
        for (String path : paths) {
            // Check if the command exists in the current directory
            File commandFile = new File(path, command);
            if (commandFile.isFile() && commandFile.canExecute()) {
                return true; // Command exists and is executable
            }
        }
        return false; // Command isn't found in any PATH directories
    }


    /**
     * Validates if the system is running in EFI mode.
     *
     * @return True if the system is running in EFI mode; otherwise, false.
     */
    public static boolean isSystemEfi() {
        return new File("/sys/firmware/efi").exists();
    }


    /**
     * Check if the system is x86_84 or amd84
     */
    public static boolean isSystemAmd64() {
        String arch = System.getProperty("os.arch").toLowerCase();
        return arch.equals("x86_64") || arch.equals("amd64");
    }


    /**
     * Check if Limine ships a UEFI binary for this architecture.
     * Limine provides BOOTX64/BOOTIA32/BOOTAA64/BOOTRISCV64/BOOTLOONGARCH64,
     * so gating entry management on x86_64 alone is unnecessarily narrow.
     */
    public static boolean isSystemSupportedArch() {
        String arch = System.getProperty("os.arch").toLowerCase();
        return arch.equals("x86_64") || arch.equals("amd64")
                || arch.equals("aarch64") || arch.equals("arm64")
                || arch.equals("riscv64") || arch.equals("loongarch64");
    }


    /**
     * Validates if the given path is a valid boot partition using FAT32.
     *
     * @param path The path to validate (e.g., "/boot/efi").
     * @return True if the path is a valid FAT32 partition; otherwise, false.
     */
    public static boolean validateVfatPartition(String path) {
        Path bootPath = Path.of(path);
        if (!Files.isDirectory(bootPath)) {
            errorMessage("Boot partition path '" + path + "' does not exist or is not a directory.");
            return false;
        }
        try {
            String fileSystemType = Files.getFileStore(bootPath).type();
            if (!fileSystemType.equalsIgnoreCase("vfat")) {
                errorMessage("Boot partition '" + path + "' is not a FAT32 (vfat) filesystem.");
                return false;
            }
        } catch (IOException e) {
            errorMessage("Cannot determine filesystem type for '" + path + "': " + e.getMessage());
            return false;
        }
        return true;
    }


    /**
     * Returns the path with correct letter casing needed by Limine.
     * FAT32 and ISO 9660  are case-insensitive, so their segments are adjusted to match the on-disk casing.
     * Limine requires an exact case-sensitive path, otherwise booting will fail.
     *
     * @param path The input file path, which may have incorrect casing.
     * @return The corrected case-sensitive path, or null if the file does not exist.
     */
    public static String correctCaseSensitivePath(String path) {
        File file = new File(path);
        if (!file.exists()) {
            return null; // File does not exist
        }

        // Build ordered list of path segments from root to target
        List<File> segments = new ArrayList<>();
        File current = file;
        while (current != null) {
            segments.addFirst(current);
            current = current.getParentFile();
        }
        List<String> correctedParts = new ArrayList<>(segments.size());
        for (File segment : segments) {
            File parent = segment.getParentFile();
            // Skip root "/" as it has no parent and needs no correction
            if (parent == null) continue;

            if (isCaseInsensitiveFs(parent)) {
                // fat32 is case-insensitive: resolve the real on-disk name
                File[] siblings = parent.listFiles();
                String correctedName = segment.getName(); // fallback
                if (siblings != null) {
                    for (File sibling : siblings) {
                        if (sibling.getName().equalsIgnoreCase(segment.getName())) {
                            correctedName = sibling.getName();
                            break;
                        }
                    }
                }
                correctedParts.add(correctedName);
            } else {
                // Native FS (ext4, btrfs, ...) is case-sensitive, keep name as-is
                correctedParts.add(segment.getName());
            }
        }
        return File.separator + String.join(File.separator, correctedParts);
    }


    public static String findBootPartition() {
        String[] mounts = {"/efi", "/boot", "/boot/efi", "/limine"};
        for (String mount : mounts) {
            Path path = Path.of(mount);
            if (!Files.isDirectory(path)) {
                continue;
            }
            boolean isVfat;
            try {
                isVfat = Files.getFileStore(path).type().equalsIgnoreCase("vfat");
            } catch (IOException e) {
                isVfat = false;
            }
            if (isVfat) {
                return mount;
            }
        }
        return null;
    }


    public static boolean isCaseInsensitiveFs(File file) {
        try {
            String type = Files.getFileStore(file.toPath()).type().toLowerCase();
            return type.equals("vfat") || type.equals("iso9660");
        } catch (Exception e) {
            // Gracefully handle permission errors or unavailable filesystem info
            return false;
        }
    }


    /**
     * Validates if a given filename conforms to the rules of FAT32 filenames.
     * FAT32 filenames must adhere to specific restrictions such as length, allowed
     * characters, and cannot start or end with a dot or space.
     *
     * @param name The filename to validate.
     * @return True if the filename is valid, according to FAT32 rules; false otherwise.
     */
    public static boolean isValidFat32Name(String name) {
        // Regular expression to validate FAT32 filenames
        Pattern FAT32_VALID_NAME_PATTERN = Pattern.compile(
                "^(?![.\\-\\s])" +      // Cannot start with a dot, hyphen, or space
                        "[a-zA-Z0-9._-]+" + // Only English letters, digits, underscores, dots, and hyphens
                        "(?<![.\\-\\s])$"  // Cannot end with a dot, hyphen, or space
        );
        // FAT32 filenames are limited to 255 characters and cannot contain invalid characters.
        if (name == null || name.isBlank() || name.length() > 99) {
            return false;
        }
        return FAT32_VALID_NAME_PATTERN.matcher(name).matches();
    }


    /**
     * Verifies if the file is older than the specified number of hours.
     *
     * @param filePath Path to the file
     * @param hours    the number of hours to compare
     * @return true if the file is older than the specified hours, false otherwise.
     */
    public static boolean isFileOlderThan(String filePath, int hours) {
        File file = new File(filePath);
        long lastModified = file.lastModified();
        if (lastModified == 0L) {
            // File does not exist or the timestamp is invalid
            return false;
        }
        long now = System.currentTimeMillis();
        long diffMillis = now - lastModified;
        long thresholdMillis = hours * 3600_000L;
        return diffMillis > thresholdMillis;
    }


    public static String getMountPoint(String partUUID) {
        Output pathOutput = getCommandOutput("findmnt -no TARGET -S PARTUUID=" + partUUID, false, false);
        if (pathOutput.isSuccess()) {
            return pathOutput.text().getFirst();
        } else {
            return "";
        }
    }


    public static String getMountPointIfFat32(String filePath) {
        Path realPath = Paths.get(filePath).toAbsolutePath().normalize();
        File mountFile = new File("/proc/mounts");

        if (!mountFile.exists()) {
            return "";
        }

        String bestMountPoint = "";

        try (Stream<String> lines = Files.lines(mountFile.toPath())) {
            for (String line : (Iterable<String>) lines::iterator) {
                String[] parts = line.split(" ");
                if (parts.length < 3) continue;

                String mountPoint = parts[1];
                String fsType = parts[2];

                if (!"vfat".equalsIgnoreCase(fsType) && !"iso9660".equalsIgnoreCase(fsType)) {
                    continue;
                }
                if (realPath.startsWith(Paths.get(mountPoint)) && mountPoint.length() > bestMountPoint.length()) {
                    bestMountPoint = mountPoint;
                }
            }
        } catch (IOException ignored) {
        }
        return bestMountPoint;
    }


    public static String removeSurroundingSlashes(String path) {
        if (path == null || path.isEmpty()) {
            return path;
        }
        return path.replaceAll("^/+", "").replaceAll("/+$", "").trim();
    }


    /**
     * Get a type of file system of the mount point
     *
     * @param mountPoint It is the mount path.
     * @return file system type.
     */
    public static String getFileSystemType(String mountPoint, boolean checkDirectory) {
        File path = new File(mountPoint);
        if (!path.exists()) {
            errorMessage("The specified path '" + path + "' does not exist.");
            return "";
        }
        if (checkDirectory && !path.isDirectory()) {
            errorMessage("The specified path '" + path + "' is not a directory.");
            return "";
        }
        try {
            FileStore store = Files.getFileStore(Paths.get(mountPoint));
            return store.type();
        } catch (IOException e) {
            errorMessage("Error checking filesystem type of the path '" + mountPoint + "' : " + e.getMessage());
            return "";
        }
    }


    /**
     * Get partition UUID of the mount point
     *
     * @param mountPoint It is the mount path.
     * @return partition UUID.
     */
    public static String getPartitionUUID(String mountPoint) {
        Output uuidOutput = getCommandOutput("findmnt -no PARTUUID --mountpoint " + mountPoint, true, true);
        if (uuidOutput.isSuccess()) {
            return uuidOutput.text().getFirst();
        } else {
            return "";
        }
    }

    public static void infoMessage(String message) {
        infoMessage(message, null);
    }

    public static void infoMessage(String message, String output) {
        if (output == null || output.isEmpty()) {
            System.out.println(ConsoleColor.WHITE_BOLD + message + ConsoleColor.RESET);
        } else if (!Config.QUIET) {
            System.out.println(ConsoleColor.GREEN_BOLD + message + ConsoleColor.RESET + " " + output);
        }
    }

    public static void warnMessage(String message) {
        warnMessage(message, null);
    }

    public static void warnMessage(String message, String output) {
        if (output == null || output.isEmpty()) {
            System.out.println(ConsoleColor.YELLOW_BOLD + message + ConsoleColor.RESET);
        } else {
            System.out.println(ConsoleColor.YELLOW_BOLD + message + ConsoleColor.RESET + " " + output);
        }
    }

    public static void errorMessage(String message) {
        errorMessage(message, null);
    }

    public static void errorMessage(String message, String output) {
        if (output == null || output.isEmpty()) {
            System.err.println(ConsoleColor.RED_BOLD + message + ConsoleColor.RESET);
            Utility.loggerSend(message, LogLevel.ERROR);
        } else {
            System.err.println(ConsoleColor.RED_BOLD + message + ConsoleColor.RESET + " " + output);
            Utility.loggerSend(message + " " + output, LogLevel.ERROR);
        }
    }

    public static void exitWithError(String message) {
        exitWithError(message, null);
    }

    public static void exitWithError(String message, String output) {
        errorMessage(message, output);
        System.exit(1);
    }


    public static String removeSurrounding(String str, String delimiter) {
        if (str != null && str.length() >= 2 && str.startsWith(delimiter) && str.endsWith(delimiter)) {
            return str.substring(delimiter.length(), str.length() - delimiter.length());
        }
        return str;
    }

    public static boolean startsWithIgnoreCase(String str, String search) {
        if (str == null || search == null) {
            return false;
        }
        return str.toLowerCase().startsWith(search.toLowerCase());
    }
}
