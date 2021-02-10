from interpreters import PageInterpreter

# TODO: predict h1 headers by this condition:
#  if a non-empty line is preceded and succeeded by at least one empty line, then it might be a h1 header
# TODO: predict match description type: either TeamA 0-0 TeamB or TeamA - TeamB 0-0
# TODO: replace default topscorer nationality with "missing" flag from Wikipedia

# example call
PageInterpreter("tur", 1989).header("final table").table().run()
