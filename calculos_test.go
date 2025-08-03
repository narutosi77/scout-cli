package main

import "testing"

// TestSumar es la función que prueba nuestra función Sumar.
// Su nombre debe empezar con "Test".
func TestSumar(t *testing.T) {
    resultado := Sumar(2, 3)
    esperado := 5

    // Comparamos el resultado obtenido con el resultado esperado.
    if resultado != esperado {
        // Si no son iguales, la prueba falla y muestra un error.
        t.Errorf("Resultado incorrecto: se obtuvo %d, se esperaba %d", resultado, esperado)
    }
}