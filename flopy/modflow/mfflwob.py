import numpy as np
from ..pakbase import Package


class ModflowFlwob(Package):
    '''
    Head-dependent flow boundary Observation package class

    Parameters
    ----------
    nqfb : int
        Number of cell groups for the head-dependent flow boundary observations
    nqcfb : int
        Greater than or equal to the total number of cells in all cell groups
    nqtfb : int
        Total number of head-dependent flow boundary observations for all cell
        groups
    iufbobsv : int
        unit number where output is saved
    tomultfb : float
        Time-offset multiplier for head-dependent flow boundary observations.
        The product of tomultfb and toffset must produce a time value in units
        consistent with other model input. tomultfb can be dimensionless or can
        be used to convert the units of toffset to the time unit used in the
        simulation.
    nqobfb : int list of length nqfb
        The number of times at which flows are observed for the group of cells
    nqclfb : int list of length nqfb
        Is a flag, and the absolute value of nqclfb is the number of cells in
        the group.  If nqclfb is less than zero, factor = 1.0 for all cells in
        the group.
    obsnam : string list of length nqtfb
        Observation name
    irefsp : int of length nqtfb
        Stress period to which the observation time is referenced. The reference
        point is the beginning of the specified stress period.
    toffset : float list of length nqtfb
        Is the time from the beginning of the stress period irefsp to the time
        of the observation.  toffset must be in units such that the product of
        toffset and tomultfb are consistent with other model input.  For steady
        state observations, specify irefsp as the steady state stress period
        and toffset less than or equal to perlen of the stress period.  If
        perlen is zero, set toffset to zero.  If the observation falls within a
        time step, linearly interpolation is used between values at the
        beginning and end of the time step.
    flwobs : float list of length nqtfb
        Observed flow value from the head-dependent flow boundary into the
        aquifer (+) or the flow from the aquifer into the boundary (-)
    layer : int list of length(nqfb, nqclfb)
        layer index for the cell included in the cell group
    row : int list of length(nqfb, nqclfb)
        row index for the cell included in the cell group
    column : int list of length(nqfb, nqclfb)
        column index of the cell included in the cell group
    factor : float list of length(nqfb, nqclfb)
        Is the portion of the simulated gain or loss in the cell that is
        included in the total gain or loss for this cell group (fn of eq. 5).
    flowtype : string
        String that corresponds to the head-dependent flow boundary condition
        type (CHD, GHB, DRN, RIV)
    extension : list of string
        Filename extension (default is ['chob','obc','gbob','obg','drob','obd',
                                        'rvob','obr'])
    unitnumber : list of int
        File unit number (default is [40, 140, 41, 141, 42, 142, 43, 143])


    Attributes
    ----------

    Methods
    -------

    See Also
    --------

    Notes

    '''

    def __init__(self, model, nqfb=0, nqcfb=0, nqtfb=0, iufbobsv=0,
                 tomultfb=1.0, nqobfb=[], nqclfb=[], obsnam=[], irefsp=[],
                 toffset=[], flwobs=[], layer=[], row=[], column=[], factor=[],
                 flowtype=None,
                 extension=['chob', 'obc', 'gbob', 'obg', 'drob',
                            'obd', 'rvob', 'obr'],
                 unitnumber=[40, 140, 41, 141, 42, 142,
                             43, 143]):

        """ Package constructor
        """
        if flowtype.upper().strip() == 'CHD':
            name = ['CHOB', 'DATA']
            extension = extension[0:2]
            unitnumber = unitnumber[0:2]
            iufbobsv = unitnumber[1]
            self.url = 'chob.htm'
            self.heading = '# CHOB for MODFLOW, generated by Flopy.'
        elif flowtype.upper().strip() == 'GHB':
            name = ['GBOB', 'DATA']
            extension = extension[2:4]
            unitnumber = unitnumber[2:4]
            iufbobsv = unitnumber[1]
            self.url = 'gbob.htm'
            self.heading = '# GBOB for MODFLOW, generated by Flopy.'
        elif flowtype.upper().strip() == 'DRN':
            name = ['DROB', 'DATA']
            extension = extension[4:6]
            unitnumber = unitnumber[4:6]
            iufbobsv = unitnumber[1]
            self.url = 'drob.htm'
            self.heading = '# DROB for MODFLOW, generated by Flopy.'
        elif flowtype.upper().strip() == 'RIV':
            name = ['RVOB', 'DATA']
            extension = extension[6:8]
            unitnumber = unitnumber[6:8]
            iufbobsv = unitnumber[1]
            self.url = 'rvob.htm'
            self.heading = '# RVOB for MODFLOW, generated by Flopy.'
        # add else here and give an error if there is no match

        Package.__init__(self, model, extension, name, unitnumber,
                         allowDuplicates=True)

        self.nqfb = nqfb
        self.nqcfb = nqcfb
        self.nqtfb = nqtfb
        self.iufbobsv = iufbobsv
        self.tomultfb = tomultfb
        self.nqobfb = nqobfb
        self.nqclfb = nqclfb
        self.obsnam = obsnam
        self.irefsp = irefsp
        self.toffset = toffset
        self.flwobs = flwobs
        self.layer = layer
        self.row = row
        self.column = column
        self.factor = factor

        # -create empty arrays of the correct size
        # self.obsnam = np.empty((self.nh), dtype='str')
        self.layer = np.zeros((self.nqfb, max(self.nqclfb)), dtype='int32')
        self.row = np.zeros((self.nqfb, max(self.nqclfb)), dtype='int32')
        self.column = np.zeros((self.nqfb, max(self.nqclfb)), dtype='int32')
        self.factor = np.zeros((self.nqfb, max(self.nqclfb)), dtype='float32')
        self.nqobfb = np.zeros((self.nqfb), dtype='int32')
        self.nqclfb = np.zeros((self.nqfb), dtype='int32')
        self.irefsp = np.zeros((self.nqtfb), dtype='int32')
        self.toffset = np.zeros((self.nqtfb), dtype='float32')
        self.flwobs = np.zeros((self.nqtfb), dtype='float32')

        # -assign values to arrays

        self.nqobfb[:] = nqobfb
        self.nqclfb[:] = nqclfb
        self.obsnam[:] = obsnam
        self.irefsp[:] = irefsp
        self.toffset[:] = toffset
        self.flwobs[:] = flwobs
        for i in range(self.nqfb):
            self.layer[i, :len(layer[i])] = layer[i]
            self.row[i, :len(row[i])] = row[i]
            self.column[i, :len(column[i])] = column[i]
            self.factor[i, :len(factor[i])] = factor[i]

        # putting in some more checks here


        # add checks for input compliance (obsnam length, etc.)
        self.parent.add_package(self)

    def write_file(self):
        """
        Write the package file

        Returns
        -------
        None

        """
        # -open file for writing
        f_fbob = open(self.fn_path, 'w')

        # -write header
        f_fbob.write('%s\n' % (self.heading))

        # -write sections 1 & 2 : NOTE- what about NOPRINT?
        f_fbob.write('%10i%10i%10i%10i\n' % (self.nqfb, self.nqcfb,
                                             self.nqtfb, self.iufbobsv))
        f_fbob.write('%10e\n' % (self.tomultfb))  # check format

        # -write sections 3-5 looping through observations groups
        c = 0
        for i in range(self.nqfb):
            #        while (i < self.nqfb):
            # write section 3
            f_fbob.write('{:10d}{:10d}\n'.format(self.nqobfb[i],
                                                 self.nqclfb[i]))

            # Loop through observation times for the groups
            for j in range(self.nqobfb[i]):
                # -write section 4
                f_fbob.write(
                    '{}{:10d}{:10.4g}{}{:10.4g}\n'.format(self.obsnam[c],
                                                          self.irefsp[c],
                                                          self.toffset[c], ' ',
                                                          self.flwobs[c]))
                c += 1  # index variable

                # -write section 5 - NOTE- need to adjust factor for muliple obs same cell
            for j in range(abs(self.nqclfb[i])):
                if self.nqclfb[
                    i] < 0:  # set factor to 1.0 for all cells in group
                    self.factor[i, :] = 1.0
                f_fbob.write('{:10d}{:10d}{:10d}{}{:10f}\n'
                             .format(self.layer[i, j], (self.row[i, j]),
                                     self.column[i, j],
                                     ' ', self.factor[
                                         i, j]))  # note- is 10f good enough here?

        f_fbob.close()
        #
        # swm: BEGIN hack for writing standard file
        sfname = self.fn_path  # swm:hack
        sfname += '_ins'  # swm: hack
        # write header
        f_ins = open(sfname, 'w')  # swm: hack for standard file
        f_ins.write('jif @\n')  # swm: hack for standard file
        f_ins.write('StandardFile 0 1 %s\n' % (
        self.nqtfb))  # swm: hack for standard file
        for i in range(0, self.nqtfb):
            f_ins.write(
                '{}\n'.format(self.obsnam[i]))  # swm: hack for standard file

        f_ins.close()
        # swm: END hack for writing standard file

        return
