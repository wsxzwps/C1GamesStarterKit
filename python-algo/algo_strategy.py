import gamelib
import random
import math
import warnings
from sys import maxsize
import json

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.
        
        self.starter_strategy(game_state)
        self.prev_state = json.loads(turn_state)
        gamelib.debug_write(self.prev_state["events"]["damage"])
        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """
    def starter_strategy(self, game_state):
        """
        Build the C1 logo. Calling this method first prioritises
        resources to build and repair the logo before spending them 
        on anything else.
        """
        self.build_c1_logo(game_state)

        """
        Then build additional defenses.
        """
        self.build_defences(game_state)

        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)

    # Here we make the C1 Logo!
    def build_c1_logo(self, game_state):

        # starter location
        firewall_locations = [[3,13],[4,13]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
        firewall_locations = [[i,15-i] for i in range(2,5)] + [[4,12]]
        for location in firewall_locations:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        # protection construction
            # detect which location is being attacked

            # find the nearest one desctructor to build

        # filters on attacking path
        firewall_locations = [[i,15-i] for i in range(5,15)] + [[6,12]]# + [[6,13],[25,13],[27,13]] + [[int(j*2+1),12] for j in range(4,13)]#[[5,10],[6,9],[7,8],]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
        
        # if available>0, fixed number of destructors + filter pair
        firewall_locations = [[6,12]] + [[26,12]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        firewall_locations = [[5,11],[5,12]]
        for location in firewall_locations:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        firewall_locations = [[27,13],[25,13]]+[[int(j*2+1),11] for j in reversed(range(6,12))]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
            location = [location[0],location[1]+1]
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

        firewall_locations = [[26,12],[24,12],[26,13]]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)

        firewall_locations = [[int(j*2+1),11] for j in reversed(range(4,6))]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
            location = [location[0],location[1]+1]
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

        firewall_locations = [[6,13],[25,13],[26,13]]
        for location in firewall_locations:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

    def build_defences(self, game_state):
        firewall_locations = [[int(j*2),10] for j in reversed(range(4,12))]
        for location in firewall_locations:
            if game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
            location = [location[0],location[1]+2]
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)

    #     """
    #     First lets protect ourselves a little with destructors:
    #     """
    #     firewall_locations = [[0, 13], [27, 13]]
    #     for location in firewall_locations:
    #         if game_state.can_spawn(DESTRUCTOR, location):
    #             game_state.attempt_spawn(DESTRUCTOR, location)

    #     """
    #     Then lets boost our offense by building some encryptors to shield 
    #     our information units. Lets put them near the front because the 
    #     shields decay over time, so shields closer to the action 
    #     are more effective.
    #     """
    #     firewall_locations = [[3, 11], [4, 11], [5, 11]]
    #     for location in firewall_locations:
    #         if game_state.can_spawn(ENCRYPTOR, location):
    #             game_state.attempt_spawn(ENCRYPTOR, location)

    #     """
    #     Lastly lets build encryptors in random locations. Normally building 
    #     randomly is a bad idea but we'll leave it to you to figure out better 
    #     strategies. 

    #     First we get all locations on the bottom half of the map
    #     that are in the arena bounds.
    #     """
    #     all_locations = []
    #     for i in range(game_state.ARENA_SIZE):
    #         for j in range(math.floor(game_state.ARENA_SIZE / 2)):
    #             if (game_state.game_map.in_arena_bounds([i, j])):
    #                 all_locations.append([i, j])
        
    #     """
    #     Then we remove locations already occupied.
    #     """
    #     possible_locations = self.filter_blocked_locations(all_locations, game_state)

    #     """
    #     While we have cores to spend, build a random Encryptor.
    #     """
    #     while game_state.get_resource(game_state.CORES) >= game_state.type_cost(ENCRYPTOR) and len(possible_locations) > 0:
    #         # Choose a random location.
    #         location_index = random.randint(0, len(possible_locations) - 1)
    #         build_location = possible_locations[location_index]
    #         """
    #         Build it and remove the location since you can't place two 
    #         firewalls in the same location.
    #         """
    #         game_state.attempt_spawn(ENCRYPTOR, build_location)
    #         possible_locations.remove(build_location)



    def deploy_attackers(self, game_state):
        """
        First lets check if we have 10 bits, if we don't we lets wait for 
        a turn where we do.
        """
        # if (game_state.get_resource(game_state.BITS) < 10):
        #     return
        
        """
        First lets deploy an EMP long range unit to destroy firewalls for us.
        """
        # if game_state.can_spawn(EMP, [3, 10]):
        #     game_state.attempt_spawn(EMP, [3, 10])

        """
        Now lets send out 3 Pings to hopefully score, we can spawn multiple 
        information units in the same location.
        """
        # if game_state.can_spawn(EMP, [0, 13], 1):
        #     game_state.attempt_spawn(EMP, [0,13], 1)
        if game_state.can_spawn(PING, [14, 0], math.floor(game_state.get_resource(game_state.BITS))):
            game_state.attempt_spawn(PING, [14,0], math.floor(game_state.get_resource(game_state.BITS)))
        
        # if game_state.can_spawn(PING, [13, 0], math.floor(game_state.get_resource(game_state.BITS)-3)):
        #     game_state.attempt_spawn(PING, [13,0], math.floor(game_state.get_resource(game_state.BITS)-3))

        """
        NOTE: the locations we used above to spawn information units may become 
        blocked by our own firewalls. We'll leave it to you to fix that issue 
        yourselves.

        Lastly lets send out Scramblers to help destroy enemy information units.
        A complex algo would predict where the enemy is going to send units and 
        develop its strategy around that. But this algo is simple so lets just 
        send out scramblers in random locations and hope for the best.

        Firstly information units can only deploy on our edges. So lets get a 
        list of those locations.
        """
        # friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # """
        # Remove locations that are blocked by our own firewalls since we can't 
        # deploy units there.
        # """
        # deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # """
        # While we have remaining bits to spend lets send out scramblers randomly.
        # """
        # while game_state.get_resource(game_state.BITS) >= game_state.type_cost(SCRAMBLER) and len(deploy_locations) > 0:
           
        #     """
        #     Choose a random deploy location.
        #     """
        #     deploy_index = random.randint(0, len(deploy_locations) - 1)
        #     deploy_location = deploy_locations[deploy_index]
            
        #     game_state.attempt_spawn(SCRAMBLER, deploy_location)
        """
        We don't have to remove the location since multiple information 
        units can occupy the same space.
        """
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
