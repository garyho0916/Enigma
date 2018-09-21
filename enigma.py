#%%
import random

def get_key(b, a):
    alist = list(a.items())
    for (key, value) in alist:
        if value == b:
            return key

class SubsitutionTable:
    def __init__(self):
        self.cha_str = 'abcdefghijklmnopqrstuvwxyz'
        self.st_dict = {}
        
    def st_generator(self):
        '''Generate subsitution table with input character'''
        cha_list = list(range(26))
        subsitution_ls = [None for cha in range(len(cha_list))]
        for cha in cha_list:
            or_index = cha_list.index(cha)
            new_index = random.randrange(len(cha_list))
            while or_index == new_index or subsitution_ls[new_index] != None :
                    new_index = random.randrange(len(cha_list))
            subsitution_ls[new_index] = cha
        self.st_dict = dict(zip(cha_list, subsitution_ls))

class Rotor(SubsitutionTable):
    def __init__(self):
        '''position will be 0 - 25'''
        super().__init__()
        self.start_pos = None
        self.position = self.start_pos

    def rotate(self):
        if self.position != 25:
            self.position = self.position + 1
        else:
            self.position = 0

    def forward_input(self, pos):
        input_pos = (pos + self.position) % 26
        output_pos = (self.st_dict[input_pos] + self.position) % 26
        return output_pos
    
    def backward_input(self, pos):
        input_pos = (pos - self.position) % 26
        output_pos = (get_key(input_pos, self.st_dict) - self.position) % 26
        return output_pos

    def reset_pos(self):
        self.position = self.start_pos

class Reflector:
    def __init__(self):
        self.reflect_table = self.reflect_table_generator()

    def reflect_table_generator(self):
        alist = list(range(26))
        blist = alist[::-1]
        reflect_table = dict(zip(alist, blist))
        return reflect_table
    
    def reflect(self, pos):
        output_pos = self.reflect_table[pos]
        return output_pos

class Enigma:
    def __init__(self, rotors, reflector, start_pos=[0,0,0]):
        self.rotors = rotors
        self.reflector = reflector        
        
        i = 0
        for rotor in self.rotors:
            rotor.start_pos = start_pos[i]
            i += 1
    
    def encrypt(self, str):
        for rotor in self.rotors:
            rotor.reset_pos()

        encrypt_list = []
        for cha in str:
            pos = self.rotors[0].cha_str.index(cha)
            for rotor in self.rotors:
                pos = rotor.forward_input(pos)

            back_pos = self.reflector.reflect(pos)

            for rotor in self.rotors[::-1]:
                back_pos = rotor.backward_input(back_pos)
            encrypt_list.append(self.rotors[0].cha_str[back_pos])

            self.rotors[0].rotate()


        for rotor in self.rotors:
            rotor.reset_pos()

        print(''.join(encrypt_list)) 

    def decrypt(self, encrypt_str):
        for rotor in self.rotors:
            rotor.reset_pos()

        decrypt_list = []
        for cha in encrypt_str:

            pos = self.rotors[0].cha_str.index(cha)
            for rotor in self.rotors:
                pos = rotor.forward_input(pos)
            
            back_pos = self.reflector.reflect(pos)

            for rotor in self.rotors[::-1]:
                back_pos = rotor.backward_input(back_pos)
            decrypt_list.append(self.rotors[0].cha_str[back_pos])

            self.rotors[0].rotate()

        for rotor in self.rotors:
            rotor.reset_pos()

        print(''.join(decrypt_list)) 

rotor1 = Rotor()
rotor1.st_generator()
rotor2 = Rotor()
rotor2.st_generator()
rotor3 = Rotor()
rotor3.st_generator()

reflector = Reflector()

enigma_gary = Enigma([rotor1, rotor2, rotor3], reflector,start_pos=[1,2,3])
enigma_gary.encrypt('hello')