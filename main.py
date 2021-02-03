from interpreters import PageInterpreter

# TODO: predict h1 headers by this condition:
#  if a non-empty line is preceded and succeeded by at least one empty line, then it might be a h1 header
# TODO: predict match description type: either TeamA 0-0 TeamB or TeamA - TeamB 0-0


# example call
PageInterpreter("tur", 1989, "final table").table().run()
