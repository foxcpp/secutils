## scmp-confine-w
Small wrapper to make applying seccomp filters easier.

### How to use?

1. Get scmp-confine from github.com/foxcpp/secutils.
   ```
   $ go get github.com/foxcpp/secutils/scmp-confine
   $ go install github.com/foxcpp/secutils/scmp-confine
   # cp $GOBIN/scmp-confine /usr/local/bin/scmmp-confine
   ```

2. Save script below somewhere
   ```
   # curl '...' -O /usr/local/bin/scmp-confine-w
   # chmod +x /usr/local/bin/scmp-confine-w
   ```
  
3. Save comma-separated whitelist of system calls to `/etc/scmp-confine/APPLICATION` where APPLICATION is path to program with forward slashes replaced with dots and leading slash removed (`/usr/bin/mpv` is `usr.bin.mpv`).
   ```
   $ cat /etc/scmp-confine/usr.bin.firefox 
   futex,poll,recvmsg,epoll_wait,write,read,readv,sendmsg,getpid,mprotect,fdatasync,madvise,recvfrom,munmap,close,writev,gettid,fsync,open,openat,fstat,mmap,sched_yield,fcntl,socketpair,stat,dup,rt_sigreturn,ftruncate,unlink,link,wait4,statfs,lseek,sendto,access,pwrite64,pread64,getpeername,socket,connect,sendmmsg,setsockopt,ioctl,getrusage,clone,lstat,getsockname,epoll_ctl,bind,getdents,shmdt,rename,set_robust_list,fadvise64,prctl,mkdir,setpriority,fstatfs,getsockopt,getpriority,rt_sigaction,getrandom,shmget,seccomp,tgkill,readlink,getuid,sched_getaffinity,geteuid,pipe,shmat,uname,execve,dup2,rmdir,prlimit64,symlink,readahead,umask,shmctl,getgid,sysinfo,getegid,sigaltstack,getresuid,pipe2,getresgid,rt_sigprocmask,epoll_create1,inotify_add_watch,eventfd2,brk,shutdown,arch_prctl,set_tid_address,clock_getres,fallocate,inotify_init1,memfd_create,getcwd,unshare,setresuid,setresgid,setgid,setuid,exit,exit_group,select,ppoll,inotify_rm_watch,chmod,shmctl,nanosleep,sched_get_priority_min,sched_get_priority_max,inotify_init,gettimeofday,msync,fchmod,fork,splice,utime,clock_gettime,sched_setscheduler,restart_syscall,getdents64,kill,semget,semctl,semop,mlock,quotactl
   ```
  
4. Symlink scmp-confine-w to application name in /usr/local/bin

   ```
   # ln -s /usr/local/bin/scmp-confine-w /usr/local/bin/firefox
   ```
5. Make sure /usr/local/bin is in `$PATH`

6. Verify that launching application launches it with seccomp filter:
   ```
   # firefox
   [scmp-confine] Shields up! 133 syscalls allowed.
   ...
   ```

