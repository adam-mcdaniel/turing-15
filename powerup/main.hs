module Main where

factorial n
  | n == 0 = 1
  | otherwise = n * (factorial n)

main = print (factorial 5)
