scmp-confine utility
=============================

Linux kernel exposes over 300 system calls to every process in userspace. This
is giant attack surface and there is thousands of vulnerabilities found in
kernel. Fortunately Linux offers facility called seccomp which allows us to
limit system calls accessible by untrusted or insecure program.

While many more complex sandbox solutions use seccomp too, this utility
utilizes only seccomp. This way you can get another layer of protection
for your system in few minutes because you don't have have to read 
anything. If you need more powerful solution - you can use
something listed in [Related projects](#related-projects).

Installation
-------------------

```
go build
go install
```
Binary will be placed in `$GOPATH/bin/scmp-confine`

Usage
-------------------

1. Get list of system calls required by application.

   strace can help here:
   ```
   strace -qcf <program>
   ```

2. Create `/usr/local/bin/<program>` with following contents:

   ```sh
   #!/bin/sh
   scmp-confine <allowed syscalls> <program> $@
   ```

   For example:
   ```
   scmp-confine read,write,close,mmap,munmap,fstat,brk,mprotect,access,execve,arch_prctl,openat,exit_group echo 
   ```

3. Use `/usr/local/bin/<program>` instead of `/usr/bin/<program>`.

Related projects
-------------------

* [minijail](https://lwn.net/Articles/700557/)

* [firejail](https://firejail.wordpress.com/)
  >Firejail is a SUID program that reduces the risk of security breaches by
  >restricting the running environment of untrusted applications using Linux
  >namespaces and seccomp-bpf. It allows a process and all its descendants to
  >have their own private view of the globally shared kernel resources, such as
  >the network stack, process table, mount table.
