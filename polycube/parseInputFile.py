
#FUNCTION parseInputFile takes a STRING filename as a parameter and 
#parses the file.  Creates an Array of "Pieces" which can be used
#to create a new piece

def parseInputFile(filename):
   lines = [line.rstrip('\n') for line in open(filename)]
   print(lines)

   numpiece = int(lines[1])
   counter = 3
   currentcubicsize = int(lines[counter])
   #print(currentcubicsize)
   piecelist = []
   piece = []
   allpieces = []
   for num in range(numpiece):
      currentcubicsize = int(lines[counter])
      piece =[]
      new_piece = []
      piecelist = []
      for i in range(currentcubicsize):
        counter = counter + 1
        
        piecelist.append(lines[counter])
        splitpiecelist = piecelist[i].split(' ')
        new_piece = [int(i) for i in splitpiecelist]
        piece.append(new_piece)
        
      
      counter = counter + 2
      allpieces.append((piece,num))
      
       
      
      
   return allpieces











def main():

  parseInputFile('testfile')

if __name__ == '__main__':
    main()
