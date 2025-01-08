import re

class Interpreter:
    def __init__(self):
        self.variables = {}  # Przechowywanie zmiennych: {nazwa: wartość}
        self.globals = {} # Przechowywanie zmiennych globalnych: {nazwa: wartość}
        self.functions = {}  # Przechowywanie funkcji: {nazwa: (parametry, ciało)}

    def set_value_in_array(self, array, indices, value):
        ref = array
        for index in indices[:-1]:
            ref = ref[index]
        ref[indices[-1]] = value

    def execute(self, node):
        if node is None:
            return None

        node_type = node[0]

        if node_type == 'przypisz':  # Przypisanie zmiennej
            if len(node) == 3:
                _, name, value, = node
                eval_value = self.eval_expression(value)
                if name[-1] == 'G':
                    self.globals[name] = eval_value
                else:
                    self.variables[name] = eval_value
            elif len(node) == 4:
                _, name, indeks, value = node
                indiecies = []
                if isinstance(indeks, list):
                    for sub in indeks:
                        while isinstance(sub, list) and sub[0] == 'indeksowanie':
                            sub = self.eval_expression(sub)
                        while isinstance(sub, tuple) and sub[0] == 'indeksowanie':
                            sub = self.eval_expression(sub)
                        if re.match(r'[+-]?(\d+(\.\d*)?)', str(sub)) == None:
                            if sub in self.variables:
                                sub = self.variables[sub]
                            elif sub in self.globals:
                                sub = self.globals[sub]
                        indiecies.append(int(sub))
                    if name[-1] == 'G':
                        self.set_value_in_array(self.globals[name], indiecies, value)
                    else:
                        self.set_value_in_array(self.variables[name], indiecies, value)
                    return
                elif re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                    if indeks in self.variables:
                        indeks = self.variables[indeks]
                    elif indeks in self.globals:
                        indeks = self.globals[indeks]
                if name not in self.variables and name not in self.globals:
                    raise ValueError(f'Nieznana tablica: {name}')
                elif re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                    raise IndexError(f'Indeks musi być liczbą: {indeks}')
                if name in self.variables:
                    if int(indeks) >= len(self.variables[name]):
                        raise IndexError(f'Indeks większy niż długość tablicy! {name}, {indeks}')
                elif name in self.globals:
                    if int(indeks) >= len(self.globals[name]):
                        raise IndexError(f'Indeks większy niż długość tablicy! {name}, {indeks}')
                eval_value = self.eval_expression(value)
                if name[-1] == 'G':
                    self.globals[name][int(indeks)] = eval_value
                else:
                    self.variables[name][int(indeks)] = eval_value
            
        elif node_type == 'deklaracja':  # Deklaracja zmiennej
            _, name, value = node
            eval_value = self.eval_expression(value)
            if name[-1] == 'G':
                self.globals[name] = eval_value
            else:
                self.variables[name] = eval_value
            
        elif node_type == 'wypisz':  # Wypisywanie wartości
            _, value = node
            eval_value = self.eval_expression(value)
            print(eval_value)

        elif node_type == 'zwroc':  # Zwracanie wartości
            _, value = node
            return self.eval_expression(value)

        elif node_type == 'petla':  # Pętla dopóki
            _, condition, body = node
            while self.eval_expression(condition):
                for stmt in body:
                    result = self.execute(stmt)
                    if result is not None:  # Obsługa "zwróć" w pętli
                        return result

        elif node_type == 'instr_warunkowa':  # Instrukcja jeżeli
            if len(node) == 4:
                _, condition, if_body, else_body = node
            else:
                _, condition, if_body = node
                else_body = []
            if self.eval_expression(condition):
                for stmt in if_body:
                    result = self.execute(stmt)
                    if result is not None:  # Obsługa "zwróć" w "jeżeli"
                        return result
            else:
                for stmt in else_body:
                    result = self.execute(stmt)
                    if result is not None:  # Obsługa "zwróć" w "wpw"
                        return result
        elif node_type == 'funkcja':  # Definicja funkcji
            _, name, params, body = node
            self.functions[name] = (params, body)

        elif node_type == 'wywolanie':  # Wywołanie funkcji
            _, name, args = node
            if name not in self.functions:
                raise ValueError(f"Nieznana funkcja: {name}")
            params, body = self.functions[name]

            # Utwórz lokalny kontekst dla funkcji
            if len(params) != len(args):
                raise ValueError(f"Niepoprawna liczba argumentów dla funkcji {name}")
            local_scope = {param: self.eval_expression(arg) for param, arg in zip(params, args)}

            # Wykonaj ciało funkcji w lokalnym kontekście
            original_variables = self.variables
            self.variables = local_scope
            result = None
            for stmt in body:
                result = self.execute(stmt)
                if result is not None:  # Jeśli funkcja zwróci wartość
                    break
            self.variables = original_variables  # Przywróć oryginalny kontekst
            return result
        
        elif node_type == 'wpisz':
            _, name = node
            val = input()
            if re.match(r'[+-]?(\d+(\.\d*)?)', val) != None: # Użytkownik wpisał liczbę
                eval_value = self.eval_expression(float(val))
                if name[-1] == 'G':
                    self.globals[name] = eval_value
                else:
                    self.variables[name] = eval_value
            elif re.match(r'"([^"]*)"', val) != None: 
                eval_value = self.eval_expression(str(val))
                if name[-1] == 'G':
                    self.globals[name] = eval_value
                else:
                    self.variables[name] = eval_value
            else: # Użytkownik wpisał nazwę zmiennej
                if val not in self.variables:
                    raise ValueError(f'Zmienna {val} nie istnieje')
                else:
                    if name[-1] == 'G' and val[-1] == 'G':
                        self.globals[name] = self.globals[val]
                    elif name[-1] == 'G':
                        self.globals[name] = self.variables[val]
                    elif val[-1] == 'G':
                        self.variables[name] = self.globals[val]
                    else:
                        self.variables[name] = self.variables[val]
        
        else:
            raise ValueError(f"Nieobsługiwany węzeł AST: {node_type}")

    def eval_expression(self, node):
        if isinstance(node, float):  # Jeśli to liczba lub tekst
            return node
        
        elif isinstance(node, str):
            if node not in self.variables and node not in self.globals:
                if re.match(r'"([^"]*)"', node) != None:
                    return node.strip('"')
                return node
            elif node in self.variables:
                return self.variables[node]
            else:
                return self.globals[node]
            
        elif isinstance(node, list):
            return node
        
        node_type = node[0]

        if node_type == 'plus':  # Dodawanie
            _, left, right = node
            return self.eval_expression(left) + self.eval_expression(right)

        elif node_type == 'minus':  # Odejmowanie
            _, left, right = node
            return self.eval_expression(left) - self.eval_expression(right)

        elif node_type == 'razy':  # Mnożenie
            _, left, right = node
            return self.eval_expression(left) * self.eval_expression(right)

        elif node_type == 'przez':  # Dzielenie
            _, left, right = node
            return self.eval_expression(left) / self.eval_expression(right)

        elif node_type == 'mniejsze':  # Porównanie: mniejsze od
            _, left, right = node
            return self.eval_expression(left) < self.eval_expression(right)
        
        elif node_type == 'większe':  # Porównanie: większe od
            _, left, right = node
            return self.eval_expression(left) > self.eval_expression(right)

        elif node_type == 'wynosi':  # Porównanie: równe
            _, left, right = node
            return self.eval_expression(left) == self.eval_expression(right)
        
        elif node_type == 'różne':  # Porównanie: różne
            _, left, right = node
            return self.eval_expression(left) != self.eval_expression(right)
        
        elif node_type == 'indeksowanie':
            _, tab, indeks = node
            if isinstance(indeks, tuple):
                while indeks[0] == 'indeksowanie':
                    indeks = self.eval_expression(indeks)
            if isinstance(indeks, list):
                val = None
                for sub in indeks:
                    while isinstance(sub, list) and sub[0] == 'indeksowanie':
                        sub = self.eval_expression(sub)
                    while isinstance(sub, tuple) and sub[0] == 'indeksowanie':
                        sub = self.eval_expression(sub)
                    if re.match(r'[+-]?(\d+(\.\d*)?)', str(sub)) == None:
                        if sub in self.variables:
                            sub = self.variables[sub]
                        elif sub in self.globals:
                            sub = self.globals[sub]
                    if tab[-1] == 'G':
                        if val is None:
                            val = self.eval_expression(self.globals[tab][int(sub)])
                        else:
                            val = val[int(sub)]
                    else:
                        if val is None:
                            val = self.eval_expression(self.variables[tab][int(sub)])
                        else:
                            val = val[int(sub)]
                return self.eval_expression(val)
            if re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                if indeks in self.variables:
                    indeks = self.variables[indeks]
                elif indeks in self.globals:
                    indeks = self.globals[indeks]
            if tab not in self.variables and tab not in self.globals:
                raise ValueError(f'Nieznana tablica: {tab}')
            elif re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                raise IndexError(f'Indeks musi być liczbą: {indeks}')
            if tab in self.variables:
                if int(indeks) >= len(self.variables[tab]):
                    raise IndexError(f'Indeks większy niż długość tablicy! {tab}, {indeks}')
                return self.eval_expression(self.variables[tab][int(indeks)])
            elif tab in self.globals:
                if int(indeks) >= len(self.globals[tab]):
                    raise IndexError(f'Indeks większy niż długość tablicy! {tab}, {indeks}')
                return self.eval_expression(self.globals[tab][int(indeks)])

        elif node_type == 'wywolanie':  # Wywołanie funkcji
            _, name, args = node
            if name not in self.functions:
                raise ValueError(f"Nieznana funkcja: {name}")
            params, body = self.functions[name]

            # Utwórz lokalny kontekst dla funkcji
            if len(params) != len(args):
                raise ValueError(f"Niepoprawna liczba argumentów dla funkcji {name}")
            local_scope = {param: self.eval_expression(arg) for param, arg in zip(params, args)}

            # Wykonaj ciało funkcji w lokalnym kontekście
            original_variables = self.variables
            self.variables = local_scope
            result = None
            for stmt in body:
                result = self.execute(stmt)
                if result is not None:  # Jeśli funkcja zwróci wartość
                    break
            self.variables = original_variables  # Przywróć oryginalny kontekst
            return result
        
    
        elif node_type == 'dlugosc': # Sprawdzenie długości tablicy lub tekstu
            _, value = node
            return len(self.eval_expression(value))
        
        else:
            raise ValueError(f"Nieobsługiwane wyrażenie: {node}")