import os, sys


# Windows / NTFS Alternative Streams
if os.name == 'nt':
    def getxattr(file, name):
      try:
        fd = open("%s:%s" % (file, name), 'rb')
        buffer = fd.read()
        fd.close()
        return buffer.decode('UTF-8')
      except:
        return None


# Unix / xattr
elif os.name == 'posix':
  from ctypes import *
  from ctypes.util import *

  # use current process to load library
  libc = CDLL(None)

  if sys.platform.find('linux') >= 0:
    libc.getxattr.argtypes = (c_char_p, c_char_p, c_char_p, c_size_t)
    libc.getxattr.restype = c_ssize_t
    def getxattr_impl(file, name, buffer):
      return libc.getxattr(fsencode(file), fsencode('user.'+name), buffer, sizeof(buffer))

  elif sys.platform.find('darwin') >= 0:
    libc.getxattr.argtypes = (c_char_p, c_char_p, c_char_p, c_size_t, c_uint32, c_int)
    libc.getxattr.restype = c_ssize_t
    def getxattr_impl(file, name, buffer):
      return libc.getxattr(fsencode(file), fsencode(name), buffer, sizeof(buffer), 0, 0)

  elif sys.platform.find('bsd') >= 0:
    libc.extattr_get_file.argtypes = (c_char_p, c_int, c_char_p, c_char_p, c_size_t)
    libc.extattr_get_file.restype = c_ssize_t
    def getxattr_impl(file, name, buffer):
      return libc.extattr_get_file(fsencode(file), 0x1, fsencode(name), buffer, sizeof(buffer))  #define EXTATTR_NAMESPACE_USER    0x00000001


  def fsencode(file):
    return file.encode(sys.getfilesystemencoding())

  def getxattr(file, name):
    buffer = create_string_buffer(8 * 1024)  # xattr size may be limited to 4 KB or less (e.g. ext4)
    n = getxattr_impl(file, name, buffer)
    if n > 0:
      return buffer.raw[0:n].decode('UTF-8')
    else:
      return None


# python xattr.py /path/to/file net.filebot.metadata
if __name__ == "__main__":
  file = sys.argv[1]
  name = sys.argv[2]
  print(getxattr(file, name))
