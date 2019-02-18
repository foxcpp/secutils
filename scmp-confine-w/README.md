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
  
3. Save newline-separated whitelist of system calls to `/etc/scmp-confine/APPLICATION` where APPLICATION is path to program with forward slashes replaced with dots and leading slash removed (`/usr/bin/mpv` is `usr.bin.mpv`).
   ```
   $ cat /etc/scmp-confine/usr.bin.firefox 
   futex
   poll
   recvmsg
   epoll_wait
   write
   read
   readv
   sendmsg
   quotactl
   ...
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

