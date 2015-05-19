

#ifndef FASTNETTOOL_SYSTEM_DATAHANDLER_H
#define FASTNETTOOL_SYSTEM_DATAHANDLER_H

#include <vector>
#include "TTree.h"


using namespace std;

template <class Type> class DataHandler
{
  public:
  
    DataHandler( TTree* input, string branch )
    {
      init( input, branch );
    }

    /// Set value
    void setValue(const unsigned row, const unsigned col, Type value)
    {
      vec[row + (numRows*col)] = value;
    }

    ///Get array pointer
    Type* getPtr() const
    {
      return vec;
    }

    /// Access the data in the array.
    /**
     This method returns the array value in the specified indexes. This is
     necessary, since the data in the mxArray is stored in a single 1D vector,
     so this method must apply the necessary offset calculations in order to correctly
     access the data. This method can be also used to write data into the array.
     @param[in] row The row index.
     @param[in] col The collumn index.
     @return the array value at the specified position.
    */
    Type &operator()(const unsigned row, const unsigned col) const
    {
      return vec[row + (numRows*col)];
    }

    /// Access the data in the array.
    /**
     This method returns the array value in the specified position. This
     method does not apply any offset calculation. It simply returns the value
     at the specified position in the mxArray vector. This method can be also
     used to write data into the vector. This primaly to be used when the user
     wants to directly access data in the mxArray vector, or to access an specified
     row, or collumn, by means of using the methods getInit, getEnd, getInc.
     @param[in] pos The position where the data will be read or written to.
     @return the vector value at the specified position.
    */
    Type &operator()(const unsigned pos) const
    {
      return vec[pos];
    }
    
    
    /// Return the index of the begining of an specified row.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to rows, this method returns the index of the first 
     element in a row, so, together with getRowEnd and getRowInc, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the row, as well as the offset were
     previously calculated at the start of the loop.
     @param[in] row, the index of the row you want to access.
     @return The position in the mxArray vector of the first element of that row.
    */
    unsigned getRowInit(const unsigned row) const
    {
      return row;
    }


    /// Return the index of the end of an specified row.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to rows, this method returns the index of the (last+1) 
     element in a row, so, together with getRowInit and getRowInc, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the row, as well as the offset were
     previously calculated at the start of the loop.
     @param[in] row, the index of the row you want to access.
     @return The position in the mxArray vector of the (last+1) element of that row.
    */
    unsigned getRowEnd(const unsigned row) const
    {
      return (row + (numRows*numCols));
    }


    /// Return the offset to use when accessing rows.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to rows, this method returns the offset to use when accessing
     rows, so, together with getRowInit and getRowEnd, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the row, as well as the offset were
     previously calculated at the start of the loop.
     @return the offset to use when accessing rows.
    */
    unsigned getRowInc() const
    {
      return numRows;
    }


    /// Return the index of the begining of an specified collumn.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to collumn, this method returns the index of the first 
     element in a collumn, so, together with getColEnd and getColInc, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the collumn, as well as the offset were
     previously calculated at the start of the loop.
     @param[in] col, the index of the collumn you want to access.
     @return The position in the mxArray vector of the first element of that collumn.
    */
    unsigned getColInit(const unsigned col) const
    {
      return col*numRows;
    }


    /// Return the index of the end of an specified collumn.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to collumn, this method returns the index of the (last+1) 
     element in a collumn, so, together with getColInit and getColInc, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the collumn, as well as the offset were
     previously calculated at the start of the loop.
     @param[in] col, the index of the collumn you want to access.
     @return The position in the mxArray vector of the (last+1) element of that collumn.
    */
    unsigned getColEnd(const unsigned col) const
    {
      return ((col+1)*numRows);
    }


    /// Return the offset to use when accessing collumn.
    /**
     Since an overhead is generated when calculating the position of an value
     in the array using the operator(int, int) function, in order to improve
     data speed access to collumn, this method returns the offset to use when accessing
     collumn, so, together with getColInit and getColEnd, it can
     be used in a "for" loop and the data can be quicly accessed by the
     operator(int) function, since no position calculation is done, as
     long as the init and end position of the collumn, as well as the offset were
     previously calculated at the start of the loop.
     @return the offset to use when accessing collumn.
    */
    unsigned getColInc() const
    {
      return 1;
    }
    
    
    /// Return the number of row of the mxArray that we are accessing.
    unsigned getNumRows() const
    {
      return numRows;
    }
    
    
    /// Return the number of collumns of the mxArray that we are accessing.
    unsigned getNumCols() const
    {
      return numCols;
    }
    
    
    /// Calculates the position in the mxArray of the value specified by matrices coordinates.
    /**
     This method returns the position in a mxArray vector of data based on
     matricial coordinates and the matrix's number of rows. As long as you must
     specify the number of rows of the matrix, this method can be used for ALL
     kinds of mxArray data.
     @param[in] row The row index of the data.
     @param[in] col The collumn index of the data.
     @param[in] numRows The number of rows matrix we want to access has.
    */
    static unsigned getPos(const unsigned row, const unsigned col, const unsigned numRows)
    {
      return (row + (numRows*col));
    }

  private:
  
    Type *vec;
    
    /// Holds the number of rows the array has.
    unsigned numRows;
    
    /// Holds the number of collumns the array has.
    unsigned numCols;

    /// Initializes the class.
    /**
     Initializes the class internal values, by pointing the internal pointer
      to the data in the mxArray and getting the array dimensions.
    */
    void init( TTree *input, string branch )
    {
      numCols = input->GetEntries();
      std::vector<Type> *var;
      input->SetBranchAddress(branch.c_str(), &var );
      input->GetEntry(0);
      numRows = var->size();
      vec = new Type[numRows*numCols];

      for(int entry=0; entry < numCols; ++entry){
        for(int j=0; j< numRows; ++j)
          setValue(j, entry, var[j]);
      }
    }



};

#endif
