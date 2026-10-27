static int cancel_fd = -1;
static void scrub_sigint_record_progress(int signal)
{
	int ret;

	ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);
	if (ret < 0)
		perror("Scrub cancel failed");
}

static int scrub_handle_sigint_parent(void)
{
	struct sigaction sa = {
		.sa_handler = SIG_IGN,
		.sa_flags = SA_RESTART,
	};

	return sigaction(SIGINT, &sa, NULL);
}

static int scrub_handle_sigint_child(int fd)
{
	struct sigaction sa = {
		.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,
	};

	cancel_fd = fd;
	return sigaction(SIGINT, &sa, NULL);
}
