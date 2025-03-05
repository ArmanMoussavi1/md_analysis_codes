import numpy as np

class LammpsRestartParser:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_data()
        self.sections = self.identify_sections()
        self.parse_header()
        self.parse_masses()
        self.parse_atoms()
        self.parse_bonds()
        self.parse_angles()
        self.parse_velocities()

    def read_data(self):
        with open(self.filename, 'r') as file:
            return [line.strip().split() for line in file if line.strip()]

    def identify_sections(self):
        sections = {}
        for i, line in enumerate(self.data):
            if len(line) > 0 and line[0] in ['Atoms', 'Velocities', 'Bonds', 'Angles', 'Dihedrals', 'Impropers']:
                sections[line[0]] = i + 1
        return sections
    
    def parse_header(self):
        self.atom_num = int(self.data[1][0])
        self.atom_types = int(self.data[2][0])
        self.bond_num = int(self.data[3][0]) if len(self.data) > 3 else 0
        self.bond_types = int(self.data[4][0]) if len(self.data) > 4 else 0
        self.angle_num = int(self.data[5][0]) if len(self.data) > 5 else 0
        self.angle_types = int(self.data[6][0]) if len(self.data) > 6 else 0
        
        self.dimensions = np.array(self.data[7:10])[:, :2].astype(float)
        self.dimensions = np.hstack((self.dimensions, np.zeros((self.dimensions.shape[0], 1))))
        self.dimensions[:, 2] = self.dimensions[:, 1] - self.dimensions[:, 0]
    
    def parse_masses(self):
        start_index = 11
        self.masses = np.array([float(row[1]) for row in self.data[start_index:start_index + self.atom_types]])
    
    def parse_atoms(self):
        self.atom_data = []
        if 'Atoms' in self.sections:
            start = self.sections['Atoms']
            self.atom_data = np.array(self.data[start:start + self.atom_num], dtype=float)
    
    def parse_bonds(self):
        self.bond_data = []
        if 'Bonds' in self.sections:
            start = self.sections['Bonds']
            self.bond_data = np.array(self.data[start:start + self.bond_num], dtype=int)
    
    def parse_angles(self):
        self.angle_data = []
        if 'Angles' in self.sections:
            start = self.sections['Angles']
            self.angle_data = np.array(self.data[start:start + self.angle_num], dtype=int)
    
    def parse_velocities(self):
        self.velocity_data = []
        if 'Velocities' in self.sections:
            start = self.sections['Velocities']
            self.velocity_data = np.array(self.data[start:start + self.atom_num], dtype=float)

    def get_summary(self):
        return {
            'Atoms': self.atom_num,
            'Atom Types': self.atom_types,
            'Bonds': self.bond_num,
            'Bond Types': self.bond_types,
            'Angles': self.angle_num,
            'Angle Types': self.angle_types,
            'Box Dimensions': self.dimensions.tolist(),
            'Masses': self.masses.tolist(),
            'Atom Data': self.atom_data.tolist() if len(self.atom_data) > 0 else None,
            'Bond Data': self.bond_data.tolist() if len(self.bond_data) > 0 else None,
            'Angle Data': self.angle_data.tolist() if len(self.angle_data) > 0 else None,
            'Velocities': self.velocity_data.tolist() if len(self.velocity_data) > 0 else None
        }

# Example usage:
parser = LammpsRestartParser('restart.data')
print(parser.atom_data[0])