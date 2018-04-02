seccomp-bpf whitelists
========================

**Disclaimer:** Provided lists can be incomplete and cause strange behavior (usually crash) when applied.
Submit an issue and I will try to fix it (I need your dmesg log or at least steps to reproduce).

Can be applied using either `scmp-confine` or `firejail`.
For latter - add `shell none` and `seccomp.keep list,here` to `/etc/firejail/profilename.local`.
