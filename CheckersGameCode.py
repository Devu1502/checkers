# -*- coding: utf-8 -*-

import random

class Utility:
    #Bitwise operations
    @staticmethod
    def flipBit(value: int, position: int) -> int:
        return value ^ (1 << position)

    @staticmethod
    def setBit(value: int, position: int) -> int:
        return value | (1 << position)

    @staticmethod
    def clearBit(value: int, position: int) -> int:
        return value & ~(1 << position)

    @staticmethod
    def checkBit(value: int, position: int) -> int:
        return (value >> position) & 1

    @staticmethod
    def toBinary(value: int) -> str:
        return bin(value)

    @staticmethod
    def toHexadecimal(value: int) -> str:
        return hex(value)

    @staticmethod
    def toDecimal(value: int) -> int:
        return value

class BitBoard:
    def __init__(self):
      self.player1_pieces = 0x00000FFF
      self.player2_pieces = 0xFFF00000
      self.currentPlayer = 1
      self.boardSize = 8

    def print_board(self):
        #Printing the board
        print("Board: ")
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if (row + col) % 2 == 1:
                    pos = (row * 4) + (col // 2)
                    if Utility.checkBit(self.player1_pieces, pos):
                        print("1", end=" ")
                    elif Utility.checkBit(self.player2_pieces, pos):
                        print("2", end=" ")
                    else:
                        print(".", end=" ")
                else:
                    print(" ", end=" ")
            print()

    def isLegalMove(self, player, start, end):
        #Check if start or end positions are out of bounds.
        if start < 0 or start > 31 or end < 0 or end > 31:
            return False

        #Checks if Player 1 only moves forward, and Player 2 only moves backward.
        if player == 1 and end <= start:
            return False
        if player == 2 and end >= start:
            return False

        #Make sure the piece being moved belongs to the player.
        if player == 1 and not Utility.checkBit(self.player1_pieces, start):
            return False
        if player == 2 and not Utility.checkBit(self.player2_pieces, start):
            return False

        #Check if the end position is already occupied by either player.
        if Utility.checkBit(self.player1_pieces, end) or Utility.checkBit(self.player2_pieces, end):
            return False

        #Check if there’s a piece directly in front (for non-capturing moves).
        front_position = start + 4 if player == 1 else start - 4
        if front_position >= 0 and front_position <= 31:
            if Utility.checkBit(self.player1_pieces, front_position) or Utility.checkBit(self.player2_pieces, front_position):
                if abs(start - end) in {4, 5}:
                    return False

        #Allow single-step diagonal moves (adjacent cells).
        if abs(start - end) in {4, 5}:
            return True

        #Check if the move is a valid capture (two-cell diagonal jump over opponent).
        elif abs(start - end) in {7, 9}:
            mid = (start + end) // 2
            if player == 1 and Utility.checkBit(self.player2_pieces, mid):
                return True
            elif player == 2 and Utility.checkBit(self.player1_pieces, mid):
                return True

        return False


    def movePiece(self, player, start, end):
        if self.isLegalMove(player, start, end):
            if player == 1:
                self.player1_pieces = Utility.clearBit(self.player1_pieces, start)
                self.player1_pieces = Utility.setBit(self.player1_pieces, end)
            elif player == 2:
                self.player2_pieces = Utility.clearBit(self.player2_pieces, start)
                self.player2_pieces = Utility.setBit(self.player2_pieces, end)

            if abs(start - end) in {7, 9}:
              mid = (start + end) // 2
              self.capturePiece(player, mid)

            print(f"Player {player} moved from {start} to {end}.")
            self.winCondition()
        else:
            print("Illegal move.")

        #Kinging
        if player == 1 and end >= 28 and not Utility.checkBit(self.player1_kings, end):
                self.player1_pieces = Utility.clearBit(self.player1_pieces, end)
                self.player1_kings = Utility.setBit(self.player1_kings, end)
                print("Player 1 kinged!")
        elif player == 2 and end <= 3 and not Utility.checkBit(self.player2_kings, end):
                self.player2_pieces = Utility.clearBit(self.player2_pieces, end)
                self.player2_kings = Utility.setBit(self.player2_kings, end)
                print("Player 2 kinged!")

    def capturePiece(self, player, position):
        #Clears the opponent's piece at the given position if a piece gets captured.
        if player == 1:
            self.player2_pieces = Utility.clearBit(self.player2_pieces, position)
        elif player == 2:
            self.player1_pieces = Utility.clearBit(self.player1_pieces, position)
        print("Piece captured!")

    def winCondition(self):
       #Checks if either player has no pieces left to determine a win.
        if self.player1_pieces == 0:
            print("Player 2 wins!")
        elif self.player2_pieces == 0:
            print("Player 1 wins!")
        else:
            self.currentPlayer = 2 if self.currentPlayer == 1 else 1
            print(f"Player {self.currentPlayer}'s turn.")

    def validMoves(self, player):
       #Generates a list of all valid moves for the given player.
        moves = []
        for start in range(32):
            #Check each position to see if it contains the player's piece.
            if (player == 1 and Utility.checkBit(self.player1_pieces, start)) or (player == 2 and Utility.checkBit(self.player2_pieces, start)):
                for end in range(32):
                    if self.isLegalMove(player, start, end):
                        moves.append((start, end))
        return moves


def play_game():
    game = BitBoard()
    game.print_board()

    while True:
        player = game.currentPlayer #Create an object of the BitBoard game.

        #Player 1 moves (user moves)
        if player == 1:
            try:
                start = int(input("Enter the position of the piece (0-31): "))
                end = int(input("Enter the position where you want to move (0-31): "))
                game.movePiece(player, start, end)
            except ValueError:
                print("Invalid. Please enter a number between 0 and 31.")
                continue
        else:
          #Player 2 moves (computer generated at random)
            valid_moves = game.validMoves(player)
            if valid_moves:
                start, end = random.choice(valid_moves)
                game.movePiece(player, start, end)
            else:
                print("No moves left")
                break

        game.print_board()

        if game.player1_pieces == 0 or game.player2_pieces == 0:
            break


play_game()
