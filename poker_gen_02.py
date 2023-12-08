import random, os
    
class Mister_House:
    class Player:
        def __init__(self,name,money=0):
            self.name = name
            self.folded = False
            self.money = money
            self.hand = [[None,None],[None,None]]
            self.river_cards = []

        # raise (force raise for initial bet)
        def up_bet(self,house,n):
            house.bet += n
            self.money -= n
            
        # call
        def same_bet(self,house):
            self.money -= house.bet
        
        # fold
        def quitter(self):
            self.folded = True
            
        def read_card(self, card): # Temp
            # Implement this method to read individual cards
            print(f"{self.name} reads the card: {card}")

        def card_probability(self, house, target_card):
            # Calculate the probability of a specific card being on the river next
            remaining_cards = 52 - house.deck_place
            target_count = sum(1 for card in house.deck[house.deck_place:] if card == target_card)
            probability = target_count / remaining_cards
            return probability
        
        def update_hand_with_river(self, river_cards):
            # Update the player's hand with the current river cards
            self.river_cards = river_cards
        
    class agent(Player):
        #ai
        def request_action(self,house):
            if not self.folded:
                # Check the strength of the hand and make decisions
                hand_strength = self.evaluate_hand(house.turn)

                if house.bet == 0:
                    # No bets made yet, can check or bet
                    if hand_strength >= 0.3:  
                        self.up_bet(house, random.randint(10, 50))
                        print(f"{self.name} bets.")
                    else:
                        print(f"{self.name} checks.")
                else:
                    # Bets have been made, can call, raise, or fold
                    if hand_strength >= 0.4:  
                        self.up_bet(house, random.randint(10, 50))
                        print(f"{self.name} raises.")
                    elif 0.2 <= hand_strength < 0.7:
                        self.same_bet(house)
                        print(f"{self.name} calls.")
                    else:
                        self.quitter()
                        print(f"{self.name} folds.")
            
        def evaluate_hand(self, turn):
            print("Player Hand 0:", self.hand[0])
            print("Player Hand 1:", self.hand[1])
            sorted_hand = sorted(self.hand[0] + self.hand[1], key=lambda card: card[1], reverse=True)
            
            if turn == 0:
                # Initial 2-card hand evaluation
                return self.evaluate_initial_hand(sorted_hand)
            else:
                # Evaluate hand considering the river cards
                return self.evaluate_with_river(sorted_hand, self.river_cards, turn)

        # Functions to check specific hand types
        def has_straight_flush(self, hand):
            return any(self.is_straight(hand[i:i+5]) and self.is_flush(hand[i:i+5]) for i in range(len(hand)-4))

        def has_four_of_a_kind(self, hand):
            return any(hand.count(card) == 4 for card in hand)

        def has_full_house(self, hand):
            return any(hand.count(card) == 3 for card in hand) and any(hand.count(card) == 2 for card in hand)

        def has_flush(self, hand):
            return any(hand.count(card) >= 5 for card in hand)

        def has_straight(self, hand):
            return any(hand[i][1] == hand[i + 1][1] + 1 for i in range(len(hand) - 1))

        def has_three_of_a_kind(self, hand):
            return any(hand.count(card) == 3 for card in hand)

        def has_two_pair(self, hand):
            return sum(hand.count(card) == 2 for card in hand) >= 4

        def has_pair(self, hand):
            return any(hand.count(card) == 2 for card in hand)
        
        def evaluate_initial_hand(self, hand):
            # Check for same suit, pair, both high cards, or close numbers
            suits = set(card[0] for card in hand)
            if len(suits) == 1:  # Same suit
                return 0.8
            elif any(hand.count(card) == 2 for card in hand):  # Pair
                return 0.7
            elif all(card[1] >= 10 for card in hand):  # Both high cards
                return 0.6
            elif abs(hand[0][1] - hand[1][1]) <= 1:  # Close numbers
                return 0.5
            else:
                return 0.4  # Other cases    
        
        def evaluate_with_river(self, hand, river_cards, turn):
            # Evaluate hand based on the stage of the river
            if turn == 1:
                return self.evaluate_flop(hand, river_cards)
            elif turn == 2:
                return self.evaluate_turn(hand, river_cards)
            elif turn == 3:
                return self.evaluate_river(hand, river_cards)

        def evaluate_flop(self, hand, river_cards):
            if self.has_straight_flush(hand + river_cards):
                return 1.0
            elif self.has_four_of_a_kind(hand + river_cards):
                return 0.9
            elif self.has_full_house(hand + river_cards):
                return 0.8
            elif self.has_flush(hand + river_cards):
                return 0.7
            elif self.has_straight(hand + river_cards):
                return 0.6
            elif self.has_three_of_a_kind(hand + river_cards):
                return 0.5
            elif self.has_two_pair(hand + river_cards):
                return 0.4
            elif self.has_pair(hand + river_cards):
                return 0.3
            else:
                return 0.2  # High card

        def evaluate_turn(self, hand, river_cards):
            if self.has_straight_flush(hand + river_cards):
                return 1.0
            elif self.has_four_of_a_kind(hand + river_cards):
                return 0.9
            elif self.has_full_house(hand + river_cards):
                return 0.8
            elif self.has_flush(hand + river_cards):
                return 0.7
            elif self.has_straight(hand + river_cards):
                return 0.6
            elif self.has_three_of_a_kind(hand + river_cards):
                return 0.5
            elif self.has_two_pair(hand + river_cards):
                return 0.4
            elif self.has_pair(hand + river_cards):
                return 0.3
            else:
                return 0.2  # High card

        def evaluate_river(self, hand, river_cards):
            if self.has_straight_flush(hand + river_cards):
                return 1.0
            elif self.has_four_of_a_kind(hand + river_cards):
                return 0.9
            elif self.has_full_house(hand + river_cards):
                return 0.8
            elif self.has_flush(hand + river_cards):
                return 0.7
            elif self.has_straight(hand + river_cards):
                return 0.6
            elif self.has_three_of_a_kind(hand + river_cards):
                return 0.5
            elif self.has_two_pair(hand + river_cards):
                return 0.4
            elif self.has_pair(hand + river_cards):
                return 0.3
            else:
                return 0.2  # High card
            
    class user(Player):
        #user   
        def request_action(self,house):
            if house.bet == 0:
                self.req_init_bet(house)
            else:
                self.req_play(house)
        def req_init_bet(self,house):
            #ask the player for an initial bet through Maestro Class
            pass
        def req_play(self,house):
            #ask the player to raise, call, or fold
            pass
          
    def __init__(self):
        self.players = []  # all player
        self.bank = 0 # house monet=y
        self.bet = 0 # current bet on the table
        self.turn = 0 #current turn
        self.max_turn = 0 # last person
        self.table_cards = [None] * 5 # values of cards on the table 
        self.cards_flipped = [False] * 5 # which cards are face up 
        self.deck = [None]*52 # the current deck
        self.deck_place = 0 # which card is on top
        
        
    
    def setup(self,bank_value,players):
        self.players = players
        self.bank = bank_value
        self.max_turn = len(players) -1

    
    def draw(self):
    #draw top card
        temp = self.deck[self.deck_place]
        self.deck_place+=1
        return temp
    
    @staticmethod
    def create_deck():
    # create an empty deck
        deck = [] 
        # iterate through each card
        for i in range(4):
            for j in range(13):
                deck.append([i, j])
        # give it out
        random.shuffle(deck)
        return deck
        
    def deal(self):
        # shuffle
        self.deck = self.create_deck()
        # dealt to players
        for i in self.players:
            i.hand = [self.draw(),self.draw()]
        # placed on table
        for i in range(len(self.table_cards)):
            self.table_cards[i] = self.draw()
        # flip first three
        self.cards_flipped = [True,True,True,False,False]
    
    def all_turn(self):
        for i in self.players:
            if i.folded == False:
                i.request_action()
    
    def get_river(self):
        temp = []
        for i in range(len(self.table_cards)):
            if self.cards_flipped[i]:
                temp.append(self.table_cards[i])
        return temp
    
    def print_game_state(self):
        print("\nCurrent Game State:")
        for player in self.players:
            print(f"{player.name}'s Hand: {player.hand}")
        print(f"River Cards: {self.table_cards}\n")
          
class Maestro:
    # orecstrate all ui
    class Page:
        def __init__(self,name: str,desc: str,ops):
            self.name = name # page title (string)
            self.desc = desc # description (string)
            self.ops = ops # user options ([[option name,function]])
            
    class Game(Page):
        def setup_prompts(self,house: Mister_House):
            s_money = self.get_int_from_player("How much money should players start with?\n","Thats not a valid integer. Try again")            
            h_money = self.get_int_from_player("How much money should the house start with?\n","Thats not a valid integer. Try again")            
            peep_n = self.get_int_from_player("How many People are playing?\n","Thats not a valid integer. Try again")
            computer_n = self.get_int_from_player("How many Computers are playing?\n","Thats not a valid integer. Try again")
            
            users = []
            for i in range(peep_n):
                users.append(house.user("Player "+str(i),s_money))
                
            comps = []
            for i in range(computer_n):
                users.append(house.agent("Computer "+str(i),s_money))
                
            players = random.shuffle(users + comps)
            
            house.setup(h_money,players)
                                    
        def get_int_from_player(self,request: str,fail: str):
            while(True):
                try:
                    return int(input(request))
                    break
                except:
                    print(fail)
                    continue
        def get_move_from_player(self,house: Mister_House,player):
            os.system('clr')
            print("River:\n\n")
            river_str = ""
            temp = house.get_river
            for i in house.get_river:
                pass # get type and string and add it to the master string with spacing
            
            # print that big string out
            # ask player for his move
            #differuiniate intial move and in play
            
            
    def __init__(self):
        self.uni_cmds = { # commands usable on all screens
            "help":self.help,
            "quit":exit
        }
        self.Main = self.Page("Main Menu","The starting menu",{ # starting page
            "play":[self.new_page,self.game_start],
            "statistics":[self.new_page,self.stats]})
        self.stats = self.Page("Statistics","Play Stats",{ # stats page
            "back":[self.new_page,self.Main]})
        self.game_start = self.Game("Setup","Declare starting money and ai count",{}) # game holding page
        self.active_page = self.Main # set the initial page to the main menu
        
        # define cards and suits
        self.TYPE = [
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "jack",
            "queen",
            "king",
            "ace"]
        self.SUIT=[
            "heart",
            "club",
            "diamond",
            "spade"] 
    
    def new_page(self,move_to: Page): #load new page and get next move
        os.system('clr')
        self.active_page = move_to
        print(move_to.name+"\n\n\n\n")
        print("Options\n\n")
        for i in move_to.ops:
            print(str.capitalize(i)+" | ",end="")
        if type(move_to) == self.Page:
            while(True):
                nextm = str.lower(input("Select an option:\n"))
                try:
                    temp = move_to.ops[nextm]
                    temp[0](temp[1])
                    break
                except:
                    try:
                        if nextm == 'help':
                            self.uni_cmds[nextm](move_to)
                            break
                        else:
                                self.uni_cmds[nextm]()
                                break
                    except:
                        print("Invalid Option, Try Again\n\n")
                        continue
            else:
                self.play_game()
                    
        def help(self,page): # print info of current page
            print("NAME:  "+page.name+"\n")
            print("DESCRIPTION:  "+page.desc+"\n")
            print("Options\n")
            for i in move_to.ops:
                print(str.capitalize(i)+" | ",end="")
            print("\n\n\n")
            
# Test code

# Create an instance of Mister_House
house = Mister_House()

# Create players (1 user and 1 agent for simplicity)
user = Mister_House.user("John Doe", 1000)
agent = Mister_House.agent("AI Bot", 1000)

# Setup the game
house.setup(5000, [user, agent])

# Deal initial cards
house.deal()

# Simulate a few turns (replace this with your actual game logic)
for turn in range(4):  # Assuming four turns for this example
    print(f"\n--- Turn {turn + 1} ---")

    # User's turn
    user.request_action(house)
    print(f"{user.name}'s hand: {user.hand}")

    # Agent's turn
    print(f"{agent.name}'s hand: {agent.hand}")
    agent.request_action(house)
    print(f"{agent.name}'s hand: {agent.hand}")

    # Display river cards
    print(f"River cards: {house.table_cards}")

# Evaluate final hands
user_final_strength = user.evaluate_hand(house.turn)
agent_final_strength = agent.evaluate_hand(house.turn)

# Display final hand strengths
print(f"\nFinal hand strength for {user.name}: {user_final_strength}")
print(f"Final hand strength for {agent.name}: {agent_final_strength}")