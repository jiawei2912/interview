import random
import time

class BitVector():
    # Assuming an int in Python is initially initialised from -5 to 256
    # Let's assume that each word represents 0 to 255 (8 bits)
    word_length = 64
    def __init__(self):
        self.words = []
    
    def has(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        if word_index >= len(self.words):
            return False
        # This line checks if the bit_index-th bit of the word_index-th word is set
        return self.words[word_index] & (1 << bit_index) != 0
    
    def add(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        while len(self.words) <= word_index:
            self.words.append(0)
        # This line sets the bit_index-th bit of the word_index-th word
        self.words[word_index] |= (1 << bit_index)
        
    def remove(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        if word_index >= len(self.words):
            return
        # This line unsets the bit_index-th bit of the word_index-th word
        self.words[word_index] &= ~(1 << bit_index)