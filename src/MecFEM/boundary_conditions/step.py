import numpy as np

from .volumetric import VolumetricForce
from .displacement import Displacement

class BCStep():
    def __init__(self, values:list[VolumetricForce | Displacement] | None=None, times:list[float] | None=None) -> None:
        if values is not None and times is not None:
            if len(values) != len(times):
                raise ValueError("Length of values and times must be the same")
        
        if (values is None and times is not None) or (values is not None and times is None):
            raise ValueError("Values cannot be None if times are provided or vice versa")

        self.values = [] if values is None else values
        self.times:list[float] = [] if times is None else times

    def add_step(self, value: VolumetricForce, time: float) -> None:
        """
        Add a new time-value pair to the BCStep.

        Parameters
        ----------
        value : ForceField
            The boundary condition value to add.
        
        time : float
            The time at which the boundary condition value is applied.
        """
        if time in self.times:
            raise ValueError("Time value already exists in BCStep")
        if time < 0:
            raise ValueError("Time must be non-negative")
        
        self.times.append(time)
        self.values.append(value)

    def interp(self, t: float) -> VolumetricForce:
        """
        Interpolates the boundary condition value at time t.

        For values greater than the last time, the last value is returned.

        For values smaller than the first time, the first value is returned.
    
        Parameters
        ----------
        t : float
            Time at which to interpolate the boundary condition value.
        """
        id_order = np.argsort(self.times)
        times = np.array(self.times)[id_order]
        values = [self.values[i] for i in id_order]

        if t < 0:
            raise ValueError("Time must be non-negative")
        
        if t <= times[0]:
            return values[0]
        elif t >= times[-1]:
            return values[-1]
        else:
            t_interp = np.interp(t, times, np.arange(len(times)))

            id_lower = np.floor(t_interp).astype(int)
            id_upper = np.ceil(t_interp).astype(int)
            weight_upper = t_interp - id_lower
            
            return values[id_lower] * (1 - weight_upper) +  values[id_upper] * weight_upper

