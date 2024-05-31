import random
import time

class BitVector():
    word_length = 64
    def __init__(self):
        self.words = []
    
    def has(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        if word_index >= len(self.words):
            return False
        return self.words[word_index] & (1 << bit_index) != 0
    
    def add(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        while len(self.words) <= word_index:
            self.words.append(0)
        self.words[word_index] |= (1 << bit_index)
        
    def remove(self, x):
        word_index = x // self.word_length
        bit_index = x % self.word_length
        if word_index >= len(self.words):
            return
        self.words[word_index] &= ~(1 << bit_index)