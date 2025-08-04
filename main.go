// main.go (en la raíz del proyecto)
package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec" // <-- IMPORTANTE: Se añade para poder ejecutar comandos externos
)

var version = flag.Bool("version", false, "Muestra la información de la versión")
var help = flag.Bool("help", false, "Muestra la información de ayuda")

func main() {
	flag.Parse()

	if *version {
		fmt.Println("scout-cli version 1.0.0")
		fmt.Println("Una interfaz de línea de comandos para Docker Scout")
		return
	}

	if *help || len(os.Args) == 1 {
		showHelp()
		return
	}

	// Usa flag.Args() para obtener los comandos que no son flags
	args := flag.Args()
	if len(args) == 0 {
		showHelp()
		return
	}

	// El primer argumento es el comando (scan, compare, etc.)
	command := args[0]
	// El resto son los argumentos para ese comando
	commandArgs := args[1:]

	switch command {
	case "scan":
		handleScan(commandArgs)
	case "compare":
		handleCompare(commandArgs)
	case "quickview":
		handleQuickview(commandArgs)
	default:
		fmt.Fprintf(os.Stderr, "Error: Comando desconocido '%s'\n\n", command)
		showHelp()
		os.Exit(1)
	}
}

func showHelp() {
	fmt.Println("Docker Scout CLI - Una herramienta para interactuar con Docker Scout.")
	fmt.Println("\nUSO:")
	fmt.Println("  scout-cli [comando] [argumentos]")
	fmt.Println("\nCOMANDOS DISPONIBLES:")
	fmt.Println("  scan      Escanea una imagen de Docker en busca de vulnerabilidades (usa 'docker scout cves')")
	fmt.Println("  compare   Compara dos imágenes de Docker (usa 'docker scout compare')")
	fmt.Println("  quickview Proporciona un análisis rápido de una imagen (usa 'docker scout quickview')")
	fmt.Println("\nBANDERAS GLOBALES (FLAGS):")
	fmt.Println("  --version Muestra la información de la versión")
	fmt.Println("  --help    Muestra este mensaje de ayuda")
	fmt.Println("\nEJEMPLOS:")
	fmt.Println("  scout-cli scan nginx:latest")
	fmt.Println("  scout-cli compare nginx:1.20 nginx:1.21")
	fmt.Println("  scout-cli quickview ubuntu:latest")
	fmt.Println("\nPara más información, visita: https://docs.docker.com/scout/")
}

// executeCommand es una función de ayuda para ejecutar comandos y mostrar su salida
func executeCommand(name string, args ...string) {
	fmt.Printf("--- Ejecutando: %s %v ---\n", name, args)
	cmd := exec.Command(name, args...)
	// Conectamos la salida y el error del comando a la salida y error de nuestro programa
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		// El error ya se habrá impreso en Stderr, así que solo salimos.
		os.Exit(1)
	}
}

func handleScan(args []string) {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "Error: Se debe especificar una imagen a escanear.")
		fmt.Fprintln(os.Stderr, "Uso: scout-cli scan <imagen>")
		os.Exit(1)
	}
	image := args[0]
	// Ejecutamos el comando real de docker scout
	executeCommand("docker", "scout", "cves", image)
}

func handleCompare(args []string) {
	if len(args) < 2 {
		fmt.Fprintln(os.Stderr, "Error: Se deben especificar dos imágenes a comparar.")
		fmt.Fprintln(os.Stderr, "Uso: scout-cli compare <imagen1> <imagen2>")
		os.Exit(1)
	}
	image1, image2 := args[0], args[1]
	// Ejecutamos el comando real de docker scout
	executeCommand("docker", "scout", "compare", image1, image2)
}

func handleQuickview(args []string) {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "Error: Se debe especificar una imagen para el análisis rápido.")
		fmt.Fprintln(os.Stderr, "Uso: scout-cli quickview <imagen>")
		os.Exit(1)
	}
	image := args[0]
	// Ejecutamos el comando real de docker scout
	executeCommand("docker", "scout", "quickview", image)
}
