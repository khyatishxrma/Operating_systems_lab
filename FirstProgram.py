import os
print("before fork")
print("current PID:", os.getpid())
pid= os.fork()
if pid==0:
    print("\nchild process")
    print("child PID:", os.getpid())
    print("parent PID:", os.getppid())
else:
    os.wait()

    print("\nparent process")
    print("parent PID:", os.getpid())
    print("child PID:", pid)
