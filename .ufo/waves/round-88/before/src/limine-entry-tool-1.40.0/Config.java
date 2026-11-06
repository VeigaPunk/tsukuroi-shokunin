package org.limine.entry.tool.objects;


public record Config(String machineID, String targetOs, String espPath, String pathFunction) {

    public static final String VERSION = "1.40.0";
    public static final String HASH_COMMAND = "b2sum";
    public static final String DEFAULT_CONFIG_FILE_PATH = "/etc/default/limine";
    public static final String LIMINE_CONFIG_FILE = "limine.conf";
    public static final String UKI_FILE_SUFFIX = ".efi";
    public static final String DEFAULT_UKI_DIR_PATH = "EFI/Linux";
    public static final String BACKUP_SUFFIX = ".old";
    public static final int DEFAULT_ORDER_PRIORITY_VALUE = 50;
    public static final boolean DEFAULT_ENTRY_OVERWRITE = false;
    public static String UKI_FILE_PREFIX = null;
    public static boolean ENABLE_OS_GENERATION = true;
    public static int CONFIG_BACKUP_THRESHOLD = 6;
    public static String SPACES = "  ";
    public static boolean ENABLE_VERIFICATION = false;
    public static String[] BOOT_ORDER = {"*", "*fallback", "Snapshots"};
    public static boolean ENABLE_SORT = false;
    public static boolean QUIET = false;
    public static boolean ENABLE_COLOR = false;
    public static boolean ENABLE_UNICODE = false;
}
