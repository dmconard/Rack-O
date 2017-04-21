"""
CS 115 Project 3 - Rack-O!
Author: Dana Conard
Description: Whoppppp
"""
import sys
import random

numCards = 60 # Total number of cards
rackSize = 10 # Number of cards in player hands

def get_top_card(card_stack):
    """
    Gets the top card from any stack of cards and returns it as an integer.
    Parameter: card_stack is a list of remaining cards in the deck or discard pile.
    Returns: value of top card (element in last index)
    """
    topcard = int(card_stack.pop())
    return topcard

def add_card_to_discard(card, discard):
    """
    Adds a card (integer) to the top of the discard pile (a list).
    Discard is the list of already discarded cards.
    Returns: None
    """
    discard.append(card)

def find_and_replace(new_card, card_to_be_replaced, hand, discard):
    """
    Finds the card to be replaced (represented by a number) in the hand and replaces it with new_card.
    The replaced card gets put on top of discard.
    Returns: None
    """
    index_of_replaced_card = 0
    for i in range(len(hand)):
        if card_to_be_replaced == hand[i]:
            index_of_replaced_card = i
    hand[index_of_replaced_card] = new_card
    discard.append(int(card_to_be_replaced))

def check_racko(hand):
    """
    Checks a hand to determine if Racko has been achieved.
    Returns: True or False
    """
    for i in range(len(hand)-1):
        if hand[i] > hand[i+1]:
            return False
    return True

def shuffle(card_stack):
    """
    Shuffles deck to start game or shuffles discard pile when deck is depleted.
    Returns: None
    """
    random.shuffle(card_stack)

def deal_initial_hands(deck):
    """
    Deals two hands of rackSize from deck.
    Returns: Two lists - human_hand and computer_hand
    """
    deal_to = rackSize
    human_hand = []
    computer_hand = []
    while len(computer_hand) != rackSize:
        deal = get_top_card(deck)
        human_hand.append(deal)
        deal = get_top_card(deck)
        computer_hand.append(deal)
    return human_hand, computer_hand

def replaceDeck(card_stack):
    """
    When deck is empty, used to shuffle discard pile as a new deck. Top card from deck is new discard pile.
    Parameters: card_stack is discard pile.
    Returns: new deck and new discard pile.
    """
    #card_stack will ONLY be discard pile
    shuffle(card_stack)
    new_deck = card_stack
    new_discard = []
    add_card_to_discard(get_top_card(new_deck), new_discard)
    return new_deck, new_discard


def computer_play(computer_hand, deck, discard):
    #Define a variable to specify the numbers that can be "allotted" to a single card in the rack
    div = numCards // rackSize

    #print lists corresponding to deck, discard pile and computer's current hand
    print("deck:", deck, sep="\n")
    print("discard pile:", discard, sep="\n")
    print()
    print("Computer's current hand:", computer_hand, sep="\n")

    #randomly decide whether to choose from the discard pile or deck
    coin = random.random() #import random for this to work
    if coin > 0.5: # Comuter chooses discard card
        # Show the discard card
        discard_card = get_top_card(discard) #Top card from the discard pile
        print("Computer: Chooses top discard card " + str(discard_card))

        #Choose a card to kick out
        #First determine index where discard_Card should be inserted

        #Estimate it by dividing the discard Card with numbers per rack (div)
        loc = (discard_card - 1) // div

        #Replace by whatever card is in computer's hand at this index
        number_of_card = computer_hand[loc]
        print("Computer: Replacing it with  " + str(number_of_card))

        #Modify the discard pile and the computer's hand
        find_and_replace(discard_card, number_of_card, computer_hand, discard)
        print("Computer's new hand: ")
        print(computer_hand)

    else:  # Computer choses deck card
        # Pick the top card from deck and print it out
        deck_card = get_top_card(deck)
        print("Computer: Chooses top card from the deck " + str(deck_card))

        coin = random.random()
        #Randomly decide whether to keep the deck card or not
        if coin > 0.5:
            # Choose a card to kick out
            # First determine index where deck card should be inserted.
            print("Computer: Chooses top deck card " + str(deck_card))

            loc = (deck_card - 1) // div
            # Replace by whatever card is in computer's hand at this index
            number_of_card = computer_hand[loc]
            print("Computer: Replacing it with " + str(number_of_card))

            #Modify the discard pile and the computer's hand
            find_and_replace(deck_card, number_of_card, computer_hand, discard)
            print("Computer's new hand is:", computer_hand, end="\n")
        else:
            print("Computer: Rejects top deck card " + str(deck_card))

            #Add card to discard pile
            add_card_to_discard(deck_card, discard)
            print("Computer's new hand is:")
            print(computer_hand)
    print()


def main():
    deck = []
    for i in range(numCards):
        deck.append(i+1)
    shuffle(deck)
    discard = []
    add_card_to_discard(get_top_card(deck), discard) # starts discard pile
    human_hand, computer_hand = deal_initial_hands(deck) # deals hands

    while check_racko(human_hand) == False and check_racko(computer_hand) == False:
        #print("deck:", deck, sep="\n")
        print("discard pile:", discard, sep="\n")
        print("Your current hand:", human_hand, sep="\n")
        topcard = int(get_top_card(discard))
        print("Do you want this discard card: " + str(topcard))
        choice_discard = input("Enter yes or no: ")
        choice_discard = choice_discard.lower()
        if choice_discard == "yes":
            card_to_be_replaced = int(input("Enter the number of the card you want to kick out: "))
            find_and_replace(topcard, card_to_be_replaced, human_hand, discard) #
            print("Your new hand is: ", human_hand, sep="\n")
            print()
        elif choice_discard == "no" :
            nextcard = get_top_card(deck)
            print("The card you get from the deck is", nextcard)
            second_choice = input("Do you want to keep this card? Enter yes or no: ")
            second_choice = second_choice.lower()
            if second_choice == "yes":
                card_to_be_replaced = int(input("Enter the number of the card you want to kick out: "))
                find_and_replace(nextcard, card_to_be_replaced, human_hand, discard)
                print("Your new hand is: ", human_hand, sep="\n", end="\n")
                print()
            else:
                add_card_to_discard(nextcard, discard)
                print("Your new hand:", human_hand, sep="\n")
                print()
        else:
            print("Choice can be only yes or no.")
            sys.exit()

        if len(deck) == 0:
            print(" \nWOAH! Deck is empty. Shuffling discard pile and using that as the new deck.")
            deck, discard = replaceDeck(discard) # replaces the discard pile as a new shuffled deck, begins discard pile

        if check_racko(human_hand) == False:
            computer_play(computer_hand, deck, discard)
            if len(deck) == 0:
                print(" \nWOAH! Deck is empty. Shuffling discard pile and using that as the new deck.")
                deck, discard = replaceDeck(discard)

    if check_racko(human_hand) == True:
        print("HUMAN WINS! with hand of", human_hand)
    elif check_racko(computer_hand) == True:
        print("COMPUTER WINS! with hand of", computer_hand)

main()