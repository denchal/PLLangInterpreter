import re

class Interpreter:
    def __init__(self):
        self.variables = {}  # Przechowywanie zmiennych: {nazwa: wartość}
        self.functions = {}  # Przechowywanie funkcji: {nazwa: (parametry, ciało)}

    def execute(self, node):
        if node is None:
            return None

        node_type = node[0]

        if node_type == 'przypisz':  # Przypisanie zmiennej
            if len(node) == 3:
                _, name, value, = node
                eval_value = self.eval_expression(value)
                self.variables[name] = float(eval_value)
            elif len(node) == 4:
                _, name, indeks, value = node
                eval_value = self.eval_expression(value)
                if name not in self.variables:
                    raise ValueError(f'Nieznana tablica: {name}')
                elif re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                    raise IndexError(f'Indeks musi być liczbą: {indeks}')
                elif not isinstance(self.variables[name], list):
                    raise IndexError(f'Próba indeksowania zmiennej! {name}')
                elif int(indeks) >= len(self.variables[name]):
                    raise IndexError(f'Indeks większy niż długość tablicy! {name}, {indeks}')
                self.variables[name][int(indeks)] = float(eval_value)
            
        elif node_type == 'deklaracja':  # Deklaracja zmiennej
            _, name, value = node
            eval_value = self.eval_expression(value)
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
            _, condition, body = node
            if len(body) == 2:
                if_body, else_body = body
            else:
                if_body, else_body = body, []
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
                self.variables[name] = eval_value
            else: # Użytkownik wpisał nazwę zmiennej
                if val not in self.variables:
                    raise ValueError(f'Zmienna {val} nie istnieje')
                else:
                    self.variables[name] = self.variables[val]
            

        else:
            raise ValueError(f"Nieobsługiwany węzeł AST: {node_type}")

    def eval_expression(self, node):
        if isinstance(node, float):  # Jeśli to liczba lub tekst
            return node
        elif isinstance(node, str):
            if node not in self.variables:
                if re.match(r'"([^"]*)"', node) != None:
                    return node.strip('"')
                return node
            return self.variables[node]
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
            if tab not in self.variables:
                raise ValueError(f'Nieznana tablica: {tab}')
            elif re.match(r'[+-]?(\d+(\.\d*)?)', str(indeks)) == None:
                raise IndexError(f'Indeks musi być liczbą: {indeks}')
            elif not isinstance(self.variables[tab], list):
                raise IndexError(f'Próba indeksowania zmiennej! {tab}')
            elif int(indeks) >= len(self.variables[tab]):
                raise IndexError(f'Indeks większy niż długość tablicy! {tab}, {indeks}')
            return self.eval_expression(self.variables[tab][int(indeks)])

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
        else:
            raise ValueError(f"Nieobsługiwane wyrażenie: {node}")