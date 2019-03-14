from typing import Optional


class HttpError(Exception):
    '''Http related error'''
    def __init__(self, 
                 message: str, 
                 code: Optional[int] = 500
    ) -> None:
        '''Create a new error class.
        
        :args:
            message: string with an human error message
            code: integer error code
        '''
        super().__init__(message)
        self.__code = code

    @property
    def error_code(self):
        return self.__code
        
