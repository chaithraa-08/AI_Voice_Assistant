from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    @property
    @abstractmethod
    def name(self):
        """
        Unique name of the tool.
        """
        pass

    @abstractmethod
    def execute(self, action, parameters):
        """
        Execute the requested action.

        Parameters
        ----------
        action : str
        parameters : dict

        Returns
        -------
        dict
        """
        pass