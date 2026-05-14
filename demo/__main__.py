#!/usr/bin/env python3
"""Demo for package-level main.

Ex.

```bash
python3 -m demo -h
```

"""

import logging

from stranded import functools

logging.basicConfig(level=logging.CRITICAL, format='%(levelname)s: %(message)s')

functools.CLI().run(__package__)
