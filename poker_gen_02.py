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

            #Unused
        def card_probability(self, house, target_card):
            # Calculate the probability of a specific card being on the river next
            remaining_cards = 52 - house.deck_place
            target_count = sum(1 for card in house.deck[house.deck_place:] if card == target_card)
            probability = target_count / remaining_cards
            return probability
        
        def evaluate_hand(self, turn):
            sorted_hand = sorted(self.hand, key=lambda index: index[1], reverse=True)

            if not sorted_hand:  # Handle empty hand
                return 0.0

            if turn == 0:
                # Initial 2-card hand evaluation
                return self.evaluate_initial_hand(sorted_hand)
            else:
                # Evaluate hand considering the river cards
                print("Test River", self.river_cards)
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
                return 0.4
            elif any(hand.count(card) == 2 for card in hand):  # Pair
                return 0.4
            elif all(card[1] >= 10 for card in hand):  # Both high cards
                return 0.3
            elif abs(hand[0][1] - hand[1][1]) <= 1:  # Close numbers
                return 0.25
            else:
                return 0.2  # Other cases    
        
        def evaluate_with_river(self, hand, river_cards, turn):
            # Evaluate hand based on the stage of the river
            if turn == 1:
                print("Eval Flop")
                return self.evaluate_flop(hand, river_cards)
            elif turn == 2:
                print("Eval Turn")
                return self.evaluate_turn(hand, river_cards)
            elif turn == 3:
                print("Eval River")
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
                return 0.95
            elif self.has_full_house(hand + river_cards):
                return 0.90
            elif self.has_flush(hand + river_cards):
                return 0.75
            elif self.has_straight(hand + river_cards):
                return 0.65
            elif self.has_three_of_a_kind(hand + river_cards):
                return 0.5
            elif self.has_two_pair(hand + river_cards):
                return 0.35
            elif self.has_pair(hand + river_cards):
                return 0.25
            else:
                return 0.1  # High card

        def evaluate_river(self, hand, river_cards):
            if self.has_straight_flush(hand + river_cards):
                return 1.0
            elif self.has_four_of_a_kind(hand + river_cards):
                return 0.95
            elif self.has_full_house(hand + river_cards):
                return 0.75
            elif self.has_flush(hand + river_cards):
                return 0.65
            elif self.has_straight(hand + river_cards):
                return 0.55
            elif self.has_three_of_a_kind(hand + river_cards):
                return 0.45
            elif self.has_two_pair(hand + river_cards):
                return 0.3
            elif self.has_pair(hand + river_cards):
                return 0.2
            else:
                return 0.1  # High card
        
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
            
    class user(Player):
        #user   
        def request_action(self, house):  # Add maestro as a parameter
            if house.bet == 0:
                self.req_init_bet(house)
            else:
                self.req_play(house)
        
        def req_init_bet(self, house):
            # Ask the player for an initial bet through Maestro Class
            bet_amount = self.get_int_from_player(f"{self.name}, enter your initial bet: ", "Invalid input. Please enter a valid integer.")
            self.up_bet(house, bet_amount)
        
        def req_play(self, house):
            # Ask the player to raise, call, or fold
            while True:
                action = input(f"{self.name}, choose your action (raise/call/fold): ").lower()
                if action in ['raise', 'call', 'fold']:
                    if action == 'raise':
                        raise_amount = self.get_int_from_player("Enter the raise amount: ", "Invalid input. Please enter a valid integer.")
                        self.up_bet(house, raise_amount)
                    elif action == 'call':
                        self.same_bet(house)
                    elif action == 'fold':
                        self.quitter()
                    break
                else:
                    print("Invalid choice. Please choose raise, call, or fold.")
        
        def get_int_from_player(self,request: str,fail: str):
            while(True):
                try:
                    return int(input(request))
                    break
                except:
                    print(fail)
                    continue
        
        def evaluate_hand(self, turn):
            sorted_hand = sorted(self.hand, key=lambda index: index[1], reverse=True)

            if not sorted_hand:  # Handle empty hand
                return 0.0

            if turn == 0:
                # Initial 2-card hand evaluation
                return self.evaluate_initial_hand(sorted_hand)
            else:
                # Evaluate hand considering the river cards
                return self.evaluate_with_river(sorted_hand, self.river_cards, turn)
          
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
    
    def deal_river(self, turn):   
        # flip first three
        if turn == 1:
            for i in range(3):
                self.table_cards[i] = self.draw()
            self.river_cards = self.table_cards.copy()
        elif turn == 2:
            self.table_cards[3] = self.draw()
            self.river_cards.append(self.table_cards[3]) # 4 cards for the turn
            print(self.table_cards[:4])
        elif turn == 3:
            self.table_cards[4] = self.draw()
            self.river_cards.append(self.table_cards[4])  # All 5 cards for the river
            print(self.table_cards[:5])
    
    def all_turn(self, maestro):  # Add maestro as a parameter
        for i in self.players:
            if i.folded == False:
                i.request_action(self, maestro)  # Pass maestro instance
    
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
        def __init__(self,name: str,desc: str,options):
            self.name = name # page title (string)
            self.desc = desc # description (string)
            self.options = options # user options ([[option name,function]])
            
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
            "quit":exit
        }
        
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
        
    def stats(self, house):
        os.system('clr')
        print("\nPlayer Statistics:")
        for player in house.players:
            print(f"{player.name} - Bets: {player.bets}, Folds: {player.folds}, All-ins: {player.all_ins}, Total Betted: {player.total_bet}")
        input("\nPress Enter to go back to the main menu.")

    
    def play_game(self):
        while True:
            os.system('clr')
            print("Main Menu:")
            print("1. Stats")
            print("2. Quit")
            print("3. Play Game")

            choice = input("Select an option (1/2/3): ")

            if choice == '1':
                self.stats(house)
            elif choice == '2':
                exit()
            elif choice == '3':
                house = Mister_House()
                player_name = input("Enter your name: ")
                user = Mister_House.user(player_name, 5000)
                ai_count = int(input("Enter the number of AI players: "))
                ai_names = ["AI Bot " + str(i) for i in range(ai_count)]
                ais = [Mister_House.agent(ai_name, 5000) for ai_name in ai_names]
                players = [user] + ais
                house.setup(5000, players)
                house.deal()

                # Simulate a few turns (replace this with your actual game logic)
                for turn in range(4):  # Assuming four turns for this example
                    print(f"\n--- Turn {turn + 1} ---")
                    
                    if turn >= 1:
                        house.deal_river(turn)

                    # User's turn
                    user.request_action(house)
                    user_hand_strength = user.evaluate_hand(turn)
                    print(f"{user.name}'s hand strength: {user_hand_strength}")
                    print(f"{user.name}'s hand: {user.hand}")

                    # AI turns
                    for ai in ais:
                        print(f"{ai.name}'s hand: {ai.hand}")
                        ai.request_action(house)
                        agent_hand_strength = ai.evaluate_hand(turn)
                        print(f"{ai.name}'s hand strength: {agent_hand_strength}")
                        print(f"{ai.name}'s hand: {ai.hand}")
                # Evaluate final hands
                print(f"River cards: {house.table_cards}")
                
                user_final_strength = user.evaluate_hand(house.turn)
                agent_final_strength = ais[0].evaluate_hand(house.turn)

                # Display final hand strengths
                print(f"\nFinal hand strength for {user.name}: {user_final_strength}")
                print(f"Final hand strength for {ais[0].name}: {agent_final_strength}")

                input("\nPress Enter to go back to the main menu.")
            else:
                print("Invalid choice. Please try again.")
            
maestro = Maestro()

while True:
    maestro.play_game()