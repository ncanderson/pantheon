#!/usr/bin/env python3

# import stuff
from pantheon.pantheons import Pantheon
from pantheon.gods import God
import pantheon.names as names
import pantheon.tokens as tokens

# main
if __name__ == "__main__":
    tokens.set_tokens_lists("fantasy")
    names.set_name_lists()
    egg_donor = God("art","philosophy","XX")
    sperm_donor = God("war","diplomacy","XY")
    pantheon = Pantheon(egg_donor,sperm_donor)
    pantheon.spawn(5)