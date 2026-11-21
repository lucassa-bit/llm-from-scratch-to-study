import torch

# Dois exemplos, cada um com três tokens.
x = torch.tensor([
    [5, 8, 2],
    [8, 2, 9],
], dtype=torch.long)

# O próximo token esperado em cada posição.
y = torch.tensor([
    [8, 2, 9],
    [2, 9, 4],
], dtype=torch.long)

print("Entradas:")
print(x)

print("\nAlvos:")
print(y)

print("\nShape de x:", x.shape)
print("Shape de y:", y.shape)
print("Tipo dos elementos:", x.dtype)
print("Dispositivo:", x.device)