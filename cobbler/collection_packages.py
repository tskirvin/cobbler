"""
A package provides a container for package resources.

Copyright 2010, Kelsey Hightower
Kelsey Hightower <kelsey.hightower@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301  USA
"""

import item_package as package
import utils
import collection
from cexceptions import CX
from utils import _

#--------------------------------------------


class Packages(collection.Collection):

    def collection_type(self):
        return "package"

    def factory_produce(self, config, seed_data):
        """
        Return a Package forged from seed_data
        """
        return package.Package(config).from_datastruct(seed_data)

    def remove(self, name, with_delete=True, with_sync=True, with_triggers=True, recursive=False, logger=None):
        """
        Remove element named 'name' from the collection
        """
        name = name.lower()
        obj = self.find(name=name)
        if obj is not None:
            if with_delete:
                if with_triggers:
                    utils.run_triggers(self.config.api, obj, "/var/lib/cobbler/triggers/delete/package/*", [], logger)

            self.lock.acquire()
            try:
                del self.listing[name]
            finally:
                self.lock.release()
            self.config.serialize_delete(self, obj)

            if with_delete:
                if with_triggers:
                    utils.run_triggers(self.config.api, obj, "/var/lib/cobbler/triggers/delete/package/post/*", [], logger)
                    utils.run_triggers(self.config.api, obj, "/var/lib/cobbler/triggers/change/*", [], logger)

            return True

        raise CX(_("cannot delete an object that does not exist: %s") % name)
