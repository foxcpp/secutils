package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"syscall"

	"github.com/seccomp/libseccomp-golang"
)

func confine(syscallIds []seccomp.ScmpSyscall, targetBinaryPath string) {
	filter, err := seccomp.NewFilter(seccomp.ActKill)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to create context:", err)
		os.Exit(2)
	}
	defer filter.Release()

    filter.AddRule(seccomp.GetSyscallByName("execve"), seccomp.ActAllow)

	for _, syscall := range syscallIds {
		err = filter.AddRule(syscall, seccomp.ActAllow)
		if err != nil {
			fmt.Fprintln(os.Stderr, "Failed to add rule:", err)
			os.Exit(2)
		}
	}

	err = filter.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to load context into kernel:", err)
		os.Exit(2)
	}
}

func main() {
	// TODO: Use os.Args[0] as program name and read syscalls set from
	// /etc/scmp-confine/<binaryname> if binary started through symlink.

	if len(os.Args) < 3 {
		fmt.Fprintln(os.Stderr, "Usage:", os.Args[0], " <syscalls> <binary> [args...]")
		os.Exit(1)
	}

	// Find binary in $PATH.
	binary, err := exec.LookPath(os.Args[2])
	if err != nil {
		fmt.Fprintln(os.Stderr, "[scmp-confine] Failed to get binary path: ", err)
		os.Exit(1)
	}

	// Decide what to pass to program.
	binaryArgs := []string{os.Args[2]}
	if len(os.Args) > 3 {
		binaryArgs = append(binaryArgs, os.Args[3:]...)
	}

	// Resolve system call names.
	syscallNames := strings.Split(os.Args[1], ",")
	syscallIds := make([]seccomp.ScmpSyscall, len(syscallNames))
	for i, syscall := range syscallNames {
		id, err := seccomp.GetSyscallFromName(syscall)
		if err != nil {
			fmt.Fprintln(os.Stderr, "[scmp-confine] Unknown system call:", syscall)
			os.Exit(1)
		}
		syscallIds[i] = id
	}

	confine(syscallIds, binary)

	fmt.Fprintln(os.Stderr, "[scmp-confine] Shields up!", len(syscallNames), "syscalls allowed.")

	env := os.Environ()
	err = syscall.Exec(binary, binaryArgs, env)
	if err != nil {
		fmt.Fprintln(os.Stderr, "[scmp-confine] Failed to exec binary:", err)
		os.Exit(3)
	}
}
