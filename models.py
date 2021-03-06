"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.
The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.
A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.
The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).
    
    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth. A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    
    def __init__(self, **info):
        """Create a new `NearEarthObject`.
        
        :param info: A dictionary of excess keyword arguments 
        supplied to the constructor.
        """
        # parse the keyword parameters
        for key, value in info.items():
            # assign the designation parameter
            if key.lower() == 'pdes':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    # if the type of value is not string
                    self.designation = str(value)
                except ValueError:
                    print(f"This {key} is not a string")

            # assign the name parameter
            elif key.lower() == 'name':
                # check the value of the parameter to avoid
                # an inappropriate or none value
                if len(value) != 0:
                    try:
                        self.name = str(value)
                    except ValueError:
                        print(f'The type of {key} is not string')
                else:
                    # if the value is none, set the value to 'None' (string)
                    self.name = None

            # assign the diameter parameter
            elif key.lower() == 'diameter':
                # check the value of the parameter to avoid
                # an inappropriate or none value
                if len(value) != 0:
                    try:
                        self.diameter = float(value)
                    except ValueError:
                        print(f'The type of {key} is not float')
                else:
                    self.diameter = float('nan')

            # assign the hazardous parameter
            elif key.lower() == 'pha':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    # if the type of value is not bool
                    self.hazardous = str(value)
                    if self.hazardous.lower() == 'y':
                        self.hazardous = True
                    else:
                        self.hazardous = False
                #print an error message
                except ValueError:
                   print(f'The type of {key} is not a string')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def new_method(self, key):
        """Print error message if key is not string."""
        print(f'The type of {key} is not a string')

    def append(self, ??pproach):
        """To add the information about a close approach.
        
        :param ??pproach: a close approach to addition
        :return: just add information
        """
        if type(??pproach) == CloseApproach:
            self.approaches.append(??pproach)

    def serialize(self):
        """To serialize an object.
        
        :return: serialized object of NearEarth
        """
        return {'designation': self.designation,
                'name': self.name,
                'diameter_km': self.diameter,
                'potentially_hazardous': self.hazardous}

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is not None:
            return f"'{self.designation} ({self.name})'"
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return f'NEO {self.name} has a diameter of {self.diameter} km ' \
                   f'and is potentially hazardous.'
        else:
            return f'NEO {self.name} has a diameter of {self.diameter} km ' \
                   f'and is not potentially hazardous.'

    def __repr__(self):
        """Return a computer-readable string representation.
        
        Return `repr(self)`, a computer-readable string representation
        of this object.
        """
        return (f"NearEarthObject(designation={self.designation}, "
                f"name={self.name}, "
                f"diameter={self.diameter}, hazardous={self.hazardous})")


class CloseApproach:
    """A close approach to Earth by an NEO.
    
    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units,
    and the relative approach velocity in kilometers per second.
    A `CloseApproach` also maintains a reference to its
    `NearEarthObject` - initally, this information
    (the NEO's primary designation) is saved in a private attribute,
    but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    
    def __init__(self, **info):
        """Create a new `CloseApproach`.
        
        :param info: A dictionary of excess keyword arguments 
        supplied to the constructor.
        """
        # parse the keyword parameters
        for key, value in info.items():
            # assign the designation parameter
            if key.lower() == 'des':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    self._designation = str(value)
                except ValueError:
                    # print an error message
                    print(f'The type of {key} is not a string')

            # assign the time parameter
            elif key.lower() == 'cd':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    self.time = str(value)
                    self.time = cd_to_datetime(self.time)
                except ValueError:
                    print(f'The type of {key} is not a string')

            # assign the distance parameter
            elif key.lower() == 'dist':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    self.distance = float(value)
                except ValueError:
                    print(f'The type of {key} is not a float')

            # assign the velocity parameter
            elif key.lower() == 'v_rel':
                # check the value of the parameter to avoid
                # an inappropriate value
                try:
                    self.velocity = float(value)
                except ValueError:
                    print(f'The type of {key} is not a float')

        self.neo = None

    def serialize(self):
        """To serialize an object.
        
        :return: serialized object of CloseApproach
        """
        return {'datetime_utc': datetime_to_str(self.time),
                'distance_au': self.distance,
                'velocity_km_s': self.velocity}

    @property
    def designation(self):
        """To access to the self._designation.
        
        :return: self._designation
        """
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of approach time.
        
        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
        in our input data set.
        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # build a formatted representation of the approach time.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f'- On {self.time}, {self.neo.fullname} approaches Earth ' \
               f'at a distance of {round(self.distance, 2)} au' \
               f' and velocity of {round(self.velocity, 2)} km/s.'

    def __repr__(self):
        """Return a computer-readable string representation.
        
        Return repr(self)`, a computer-readable string representation of
        this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
