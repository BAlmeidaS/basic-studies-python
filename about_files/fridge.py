from contextlib import closing

class RefrigeratorRaider:
    def open(self):
        print("Open fridge door.")

    def take(self, food):
        print("Finding {}...".format(food))
        print("Taking {}.".format(food))

    def close(self):
        print("Close fridge door.")

def raid_without_with(food):
    r = RefrigeratorRaider()
    r.open()
    r.take(food)
    r.close()

def raid(food):
    with closing(RefrigeratorRaider()) as r:
        r.open()
        r.take(food)
