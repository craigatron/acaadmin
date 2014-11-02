# Import production settings.
from acaadmin.settings.production import *

# Import optional local settings.
try:
  from acaadmin.settings.local import *
except ImportError:
  pass
