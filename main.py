import json

class TuringMachine:
    def __init__(self, description):
        self.initial = description["initial"]
        self.finals = set(description["final"])
        self.blank = description["white"]
        self.transitions = {}
        for t in description["transitions"]:
            self.transitions[(t["from"], t["read"])] = (t["to"], t["write"], t["dir"])

    def run(self, tape_input, max_steps=10000):
        tape = list(tape_input)
        head = 0
        state = self.initial
        steps = 0

        while steps < max_steps:
            steps += 1
            symbol = tape[head] if 0 <= head < len(tape) else self.blank
            if (state, symbol) not in self.transitions:
                break

            new_state, new_symbol, direction = self.transitions[(state, symbol)]
            if 0 <= head < len(tape):
                tape[head] = new_symbol
            else:
                tape.append(new_symbol)

            state = new_state
            head = head + (1 if direction == "R" else -1)
            if head < 0:
                tape.insert(0, self.blank)
                head = 0

            if state in self.finals:
                return True, "".join(tape).strip(self.blank)

        return False, "".join(tape).strip(self.blank)


# ---- Carregar autômatos ----
with open("duplo_bal (1).json", "r") as f:
    duplo_bal = json.load(f)

with open("igualdade.json", "r") as f:
    igualdade = json.load(f)

machines = {
    "duplo_bal": TuringMachine(duplo_bal),
    "igualdade": TuringMachine(igualdade)
}

# ---- Testes interativos ----
print("Digite uma palavra de entrada (ou 'sair' para encerrar):")
while True:
    entrada = input(" fita > ").strip()
    if entrada.lower() == "sair":
        break

    for nome, maquina in machines.items():
        aceitou, resultado = maquina.run(entrada)
        status = "ACEITA" if aceitou else "REJEITA"
        print(f"  Máquina {nome}: {status} | fita final: {resultado}")
    print("-")
