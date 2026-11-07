package org.limine.entry.tool;

import org.limine.entry.tool.objects.*;
import org.limine.entry.tool.processes.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static org.limine.entry.tool.processes.Utility.*;


public class Main {

    static void main(String[] args) throws IOException {
        // First, parse flags (e.g., --quiet, --help, --version) and store them
        List<String> remainingArgs = new ArrayList<>();
        String comment = "";
        boolean keepFiles = false;
        EntryOptions entryOptions = new EntryOptions();
        boolean isArgComment = false, isArgPriority = false;
        for (String arg : args) {
            if (isArgComment) {
                if (arg.startsWith("--")) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                } else {
                    comment = arg;
                    isArgComment = false; //Reset
                    continue;
                }
            }
            if (isArgPriority) {
                if (entryOptions.parseArg(arg, EntryOptions.Key.ORDER_PRIORITY)) {
                    isArgPriority = false; //Reset
                    continue;
                } else {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
            }
            switch (arg) {
                case "--quiet":
                    Config.QUIET = true;
                    break;
                case "--help":
                    printHelp();
                    return;
                case "--version":
                    System.out.println(ConsoleColor.GREEN + Config.VERSION + ConsoleColor.RESET);
                    return;
                case "--comment":
                    isArgComment = true;
                    break;
                case "--keep-files":
                    keepFiles = true;
                    break;
                case "--priority":
                    isArgPriority = true;
                    break;
                case "--overwrite":
                    entryOptions.setEntryOverwrite(true);
                    break;
                default:
                    remainingArgs.add(arg);
                    break;
            }
        }

        // Now, process the main command (first element of remainingArgs)
        if (remainingArgs.isEmpty()) {
            System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
            printHelp();
            return;
        }

        String command = remainingArgs.get(0);
        String kernelName;

        switch (command) {
            case "--add", "--add-kernel":
                if (remainingArgs.size() < 3) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                kernelName = remainingArgs.get(1);
                String path1 = remainingArgs.get(2);
                String path2 = remainingArgs.size() > 3 ? remainingArgs.get(3) : null;
                String fileName1 = Utility.extractFileNameFromPath(path1);
                String vmlinuzPath;
                String initramfsPath;
                String suffixName = remainingArgs.size() == 5 ? remainingArgs.get(4) : "";
                if (path2 == null) {
                    vmlinuzPath = path1;
                    initramfsPath = null;
                    suffixName = "";
                } else if (fileName1.contains("initr")) {
                    initramfsPath = path1;
                    vmlinuzPath = path2;
                } else {
                    vmlinuzPath = path1;
                    initramfsPath = path2;
                }
                addKernel(kernelName, comment, entryOptions, initramfsPath, vmlinuzPath, suffixName);
                return;

            case "--add-uki":
                if (remainingArgs.size() < 3) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                kernelName = remainingArgs.get(1);
                String ukiPath = remainingArgs.get(2);
                addUki(kernelName, comment, entryOptions, ukiPath);
                return;

            case "--add-efi":
                if (remainingArgs.size() < 3) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                String efiName = remainingArgs.get(1);
                String efiPath = remainingArgs.get(2);
                addEfi(efiName, comment, entryOptions, efiPath, true);
                return;

            case "--remove", "--remove-kernel":
                if (remainingArgs.size() != 2) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                kernelName = remainingArgs.get(1);
                if (keepFiles) {
                    removeKernelEntry(kernelName);
                } else {
                    removeKernel(kernelName, false);
                }
                return;

            case "--remove-uki":
                if (remainingArgs.size() != 2) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                kernelName = remainingArgs.get(1);
                if (keepFiles) {
                    removeKernelEntry(kernelName);
                } else {
                    removeKernel(kernelName, true);
                }
                return;

            case "--remove-entry", "--remove-os":
                if (remainingArgs.size() < 2) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                String entryPath = remainingArgs.get(1);
                int position = 1;
                if (remainingArgs.size() > 2) {
                    try {
                        position = Integer.parseInt(remainingArgs.get(2));
                    } catch (NumberFormatException ignored) {
                        exitWithError("'" + remainingArgs.get(2) + "' is an invalid position. Position must be a number.");
                    }
                }
                removeEntry(entryPath, position);
                return;

            case "--remove-efi", "--remove-efi-path":
                if (remainingArgs.size() != 2) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                String filePath = remainingArgs.get(1);
                removeEfiPath(filePath, keepFiles);
                return;

            case "--remove-all":
                List<String> kernelNames = remainingArgs.stream().filter(arg -> !arg.startsWith("--")).toList();
                removeAll(kernelNames, keepFiles);
                return;

            case "--scan":
                scanEfiEntries();
                return;

            case "--get-cmdline":
                if (remainingArgs.size() != 2) {
                    System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                    printHelp();
                    return;
                }
                kernelName = remainingArgs.get(1);
                System.out.println(BootOptions.getKernelCmdline(kernelName));
                return;

            case "--tree":
                int defaultDepth = 3;
                if (remainingArgs.size() > 1) {
                    try {
                        defaultDepth = Integer.parseInt(remainingArgs.get(1));
                    } catch (NumberFormatException ignored) {
                        warnMessage("'" + remainingArgs.get(1) + "' is an invalid depth. Depth must be a number.");
                    }
                }
                printTree(defaultDepth);
                return;

            default:
                System.err.println(ConsoleColor.RED_BOLD + "Invalid arguments" + ConsoleColor.RESET);
                printHelp();
        }
    }

    private static void printHelp() {
        System.out.println("""
                Usage: limine-entry-tool [options] [--quiet]
                
                Options:
                    --add-kernel <kernel name> <kernel path> [initramfs path] [suffix] [--comment <comment>]
                        Add a kernel entry under the current OS entry (alias: --add)
                
                    --add-uki <kernel name> <UKI path> [--comment <comment>]
                        Add a UKI entry under the current OS entry
                
                    --add-efi <name> <EFI binary path> [--comment <comment>] [--priority <number>] [--overwrite]
                        Add an EFI entry at the top level of the boot menu
                
                    --get-cmdline <kernel name> <profile name>
                        Show kernel command line
                
                    --remove-kernel <kernel name> [--keep-files]
                        Remove kernel entry under the current OS entry (alias: --remove)
                
                    --remove-uki <kernel name> [--keep-files]
                        Remove UKI entry under the current OS entry
                
                    --remove-all <kernel name...> [--keep-files]
                        Remove all kernel or UKI entries matching the given kernel names under the current OS entry
                
                    --remove-efi-path <EFI binary path> [--keep-files]
                        Remove EFI entries matching the specified file path at the top level of the boot menu (alias: --remove-efi)
                
                    --remove-entry <entry/sub-entry/... or machine-ID> <position>
                        Remove an entry by path, or remove an OS entry matching the given machine ID at the top level of the boot menu.
                        Default position: 1
                        Note: If position is 0, all matching entries will be removed (path-based mode only).
                
                    --scan
                        Scan available EFI entries for selection
                
                    --tree [depth]
                        Display the boot menu tree
                        Default depth: 3
                
                    --version
                        Show version information
                """);
    }

    private static void addKernel(String kernelName, String comment, EntryOptions kernelEntryOptions, String initramfsPath, String vmlinuzPath, String suffixName) throws IOException {
        boolean isNameValid = Utility.isValidFat32Name(kernelName + suffixName);
        if (!isNameValid) {
            exitWithError("Kernel name: '" + kernelName + suffixName + "' is invalid due to FAT32 naming rules: Spaces and other special characters are not allowed.");
            return;
        }
        kernelName = kernelName.trim();
        suffixName = suffixName.trim();
        comment = comment.trim();

        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();

        LimineReader limine = new LimineReader(config);
        LimineManager manager = new LimineManager(limine.getTargetOsNode(), config);
        manager.addKernel(kernelName, comment, kernelEntryOptions, initramfsPath, vmlinuzPath, suffixName);

        // Save
        if (manager.isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    private static void addUki(String kernelName, String comment, EntryOptions kernelEntryOptions, String ukiFilePath) throws IOException {
        if (!Utility.isSystemSupportedArch()) {
            exitWithError("Limine has no UEFI binary for this architecture");
        }
        if (!Utility.isSystemEfi()) {
            exitWithError("Your system is not using EFI mode");
        }

        boolean isNameValid = Utility.isValidFat32Name(kernelName);
        if (!isNameValid) {
            exitWithError("Kernel name: '" + kernelName + "' is invalid due to FAT32 naming rules: Spaces and other special characters are not allowed.");
            return;
        }
        kernelName = kernelName.trim();
        comment = comment.trim();

        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();

        LimineReader limine = new LimineReader(config);
        LimineManager manager = new LimineManager(limine.getTargetOsNode(), config);
        manager.addUki(kernelName, comment, kernelEntryOptions, ukiFilePath);

        // Save
        if (manager.isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    private static void addEfi(String efiName, String comment, EntryOptions kernelEntryOptions, String efiFilePath, boolean shouldCheckDevice) throws IOException {
        if (shouldCheckDevice && !Utility.isSystemSupportedArch()) {
            exitWithError("Limine has no UEFI binary for this architecture");
            return;
        }
        if (shouldCheckDevice && !Utility.isSystemEfi()) {
            exitWithError("Your system is not using EFI mode");
            return;
        }

        efiName = efiName.trim();
        comment = comment.trim();
        efiFilePath = efiFilePath.trim();

        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();
        Config.ENABLE_OS_GENERATION = false;
        LimineReader limine = new LimineReader(config);
        boolean isUpdateNeeded = LimineManager.addEfi(limine.getRootNode(), efiName, comment, kernelEntryOptions, efiFilePath, config);

        // Save
        if (isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }


    private static void removeKernel(String kernelName, boolean isUKI) throws IOException {
        boolean isNameValid = Utility.isValidFat32Name(kernelName);
        if (!isNameValid) {
            exitWithError("Kernel name: '" + kernelName + "' is invalid due to FAT32 naming rules: Spaces and other special characters are not allowed.");
            return;
        }

        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();

        LimineReader limine = new LimineReader(config);
        LimineManager manager = new LimineManager(limine.getTargetOsNode(), config);
        manager.removeKernel(kernelName.trim(), isUKI);

        // Save
        if (manager.isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    /**
     * Remove a kernel entry without deleting kernel files
     */
    private static void removeKernelEntry(String kernelName) throws IOException {
        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();

        LimineReader limine = new LimineReader(config);
        LimineManager manager = new LimineManager(limine.getTargetOsNode(), config);
        manager.removeKernelEntry(kernelName.trim());

        // Save
        if (manager.isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    private static void removeAll(List<String> kernelNames, boolean keepFiles) throws IOException {
        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();
        LimineReader limine = new LimineReader(config);
        LimineManager manager = new LimineManager(limine.getTargetOsNode(), config);
        for (String kernelName : kernelNames) {
            boolean isNameValid = Utility.isValidFat32Name(kernelName);
            if (isNameValid) {
                if (keepFiles) {
                    manager.removeKernelEntry(kernelName.trim());
                } else {
                    manager.removeKernel(kernelName.trim(), true);
                    manager.removeKernel(kernelName.trim(), false);
                }
            } else {
                errorMessage("Kernel name: '" + kernelName + "' is invalid due to FAT32 naming rules: Spaces and other special characters are not allowed.");
            }
        }
        // Save
        if (manager.isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    /**
     * Remove EFI entries matching the specified EFI binary path
     */
    private static void removeEfiPath(String efiFilePath, boolean keepFiles) throws IOException {
        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();
        Config.ENABLE_OS_GENERATION = false;
        LimineReader limine = new LimineReader(config);
        boolean isUpdateNeeded = LimineManager.removeEfiPath(limine.getRootNode(), efiFilePath, config, keepFiles);
        // Save
        if (isUpdateNeeded) {
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    /**
     * Removes entries from the boot tree.
     *
     * @param entryPath can be either:
     *                  - a path of entry/sub-entry names (e.g. "Arch Linux/Snapshots")
     *                  - or a machine ID (top-level OS entry identifier)
     * @param position  controls which matching entry is removed:
     *                  - 0: remove all matching entries
     *                  - > 0: remove only the N-th matching entry (1-based)
     */
    private static void removeEntry(String entryPath, int position) throws IOException {
        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();
        Config.ENABLE_OS_GENERATION = false;
        LimineReader limine = new LimineReader(config);
        boolean isUpdateNeeded = LimineManager.removeEntry(limine.getRootNode(), entryPath, position);
        // Save
        if (isUpdateNeeded) {
            infoMessage("Removed:", entryPath);
            LimineWriter writer = new LimineWriter(config);
            writer.backup();
            writer.save(limine.getRootNode());
        }
    }

    private static void scanEfiEntries() throws IOException {
        ConfigReader.detectColorSupport();
        Config.ENABLE_OS_GENERATION = false;
        boolean isSuccess = true;
        EfiBootEntry selectedEntry = EfiScanner.showEfiEntriesAndSelect();
        if (selectedEntry != null) {
            Config.QUIET = true;
            EntryOptions options = new EntryOptions().setPriority(20).setEntryOverwrite(true);
            String mountPoint = Utility.getMountPoint(selectedEntry.gptUuid());
            if (mountPoint.isEmpty()) {
                String tempMountPoint = "/run/let";
                Utility.ensureDirectoryExists(tempMountPoint);
                if (Utility.runCommand("mount /dev/disk/by-partuuid/" + selectedEntry.gptUuid() + " " + tempMountPoint, false, false)) {
                    String fs = Utility.getFileSystemType(tempMountPoint, true);
                    if ("vfat".equalsIgnoreCase(fs) || "iso9660".equalsIgnoreCase(fs)) {
                        addEfi(selectedEntry.name(), selectedEntry.comment(), options, tempMountPoint + selectedEntry.efiPath(), false);
                    } else {
                        isSuccess = false;
                        warnMessage("Limine does not support the filesystem:", fs + " on the boot partition");
                    }
                    Utility.runCommand("umount " + tempMountPoint, false, false);
                } else {
                    isSuccess = false;
                }
            } else {
                String fs = Utility.getFileSystemType(mountPoint, true);
                if ("vfat".equalsIgnoreCase(fs) || "iso9660".equalsIgnoreCase(fs)) {
                    addEfi(selectedEntry.name(), selectedEntry.comment(), options, mountPoint + selectedEntry.efiPath(), false);
                } else {
                    isSuccess = false;
                    warnMessage("Limine does not support the filesystem:", fs + " on the boot partition");
                }
            }
            Config.QUIET = false;
            if (isSuccess) {
                infoMessage("EFI entry added to Limine:", "\"" + selectedEntry.name() + "\", uuid(" + selectedEntry.gptUuid() + "):" + selectedEntry.efiPath());
            } else {
                System.exit(1);
            }
        } else {
            System.exit(1);
        }
    }

    private static void printTree(int depth) throws IOException {
        ConfigReader configReader = new ConfigReader();
        Config config = configReader.readConfig();
        Config.ENABLE_OS_GENERATION = false;
        new LimineReader(config).printTree(depth);
    }
}