import abc
import os

class AbstractConverter(abc.ABC):
   @abc.abstractmethod
   def convert(self, input,output):
        pass

   @abc.abstractmethod
   def Write(self, output):
       pass

   @abc.abstractmethod
   def read(self, input):
       pass
