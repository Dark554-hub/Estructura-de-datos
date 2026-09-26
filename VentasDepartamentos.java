import java.util.Scanner;

/**
 * Programa de gestión de Ventas Mensuales por Departamento (Matriz Bidimensional en Java).
 * Departamentos: Ropa, Deportes, Juguetería (3 columnas)
 * Meses: Enero a Diciembre (12 filas)
 */
public class VentasDepartamentos {

    // Arreglos de nombres de meses y departamentos para navegación y visualización
    public static final String[] MESES = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    public static final String[] DEPARTAMENTOS = {"Ropa", "Deportes", "Juguetería"};

    // Matriz bidimensional de 12 meses x 3 departamentos
    private double[][] matrizVentas;

    public VentasDepartamentos() {
        this.matrizVentas = new double[12][3];
    }

    /**
     * Convierte un mes (String o número) en índice de fila (0-11).
     */
    private int obtenerIndiceMes(String mesInput) {
        try {
            int numMes = Integer.parseInt(mesInput.trim());
            if (numMes >= 1 && numMes <= 12) {
                return numMes - 1;
            }
        } catch (NumberFormatException e) {
            String mesTrimmed = mesInput.trim();
            for (int i = 0; i < MESES.length; i++) {
                if (MESES[i].equalsIgnoreCase(mesTrimmed)) {
                    return i;
                }
            }
        }
        return -1;
    }

    /**
     * Convierte un departamento (String o número) en índice de columna (0-2).
     */
    private int obtenerIndiceDepartamento(String depInput) {
        try {
            int numDep = Integer.parseInt(depInput.trim());
            if (numDep >= 1 && numDep <= 3) {
                return numDep - 1;
            }
        } catch (NumberFormatException e) {
            String depTrimmed = depInput.trim();
            for (int i = 0; i < DEPARTAMENTOS.length; i++) {
                if (DEPARTAMENTOS[i].equalsIgnoreCase(depTrimmed)) {
                    return i;
                }
            }
        }
        return -1;
    }

    /**
     * 1. Método para insertar o actualizar elementos en el arreglo bidimensional.
     */
    public boolean insertarVenta(String mes, String departamento, double monto) {
        int idxMes = obtenerIndiceMes(mes);
        int idxDep = obtenerIndiceDepartamento(departamento);

        if (idxMes == -1 || idxDep == -1) {
            System.out.println("Error: Mes o Departamento inválido.");
            return false;
        }
        if (monto < 0) {
            System.out.println("Error: El monto no puede ser negativo.");
            return false;
        }

        matrizVentas[idxMes][idxDep] = monto;
        System.out.printf("ÉXITO: Se insertó la venta de $%.2f en %s (%s).\n",
                monto, DEPARTAMENTOS[idxDep], MESES[idxMes]);
        return true;
    }

    /**
     * 2. Método que permite buscar algún elemento en particular (venta por mes y departamento).
     */
    public Double buscarVenta(String mes, String departamento) {
        int idxMes = obtenerIndiceMes(mes);
        int idxDep = obtenerIndiceDepartamento(departamento);

        if (idxMes == -1 || idxDep == -1) {
            System.out.println("Error: Mes o Departamento inválido.");
            return null;
        }

        double monto = matrizVentas[idxMes][idxDep];
        System.out.printf("RESULTADO: La venta en %s para %s es: $%.2f\n",
                MESES[idxMes], DEPARTAMENTOS[idxDep], monto);
        return monto;
    }

    /**
     * 3. Método que permite eliminar una venta en particular de algún departamento.
     */
    public boolean eliminarVenta(String mes, String departamento) {
        int idxMes = obtenerIndiceMes(mes);
        int idxDep = obtenerIndiceDepartamento(departamento);

        if (idxMes == -1 || idxDep == -1) {
            System.out.println("Error: Mes o Departamento inválido.");
            return false;
        }

        double montoAnterior = matrizVentas[idxMes][idxDep];
        matrizVentas[idxMes][idxDep] = 0.0;
        System.out.printf("ÉXITO: Se eliminó la venta de %s en %s (Monto anterior: $%.2f).\n",
                DEPARTAMENTOS[idxDep], MESES[idxMes], montoAnterior);
        return true;
    }

    /**
     * Muestra la tabla completa de ventas.
     */
    public void mostrarTabla() {
        System.out.println("\n============================================================");
        System.out.printf("%38s\n", "TABLA DE VENTAS MENSUALES");
        System.out.println("============================================================");
        System.out.printf("%-15s", "Mes");
        for (String dep : DEPARTAMENTOS) {
            System.out.printf("%15s", dep);
        }
        System.out.println("\n------------------------------------------------------------");

        for (int i = 0; i < MESES.length; i++) {
            System.out.printf("%-15s", MESES[i]);
            for (int j = 0; j < DEPARTAMENTOS.length; j++) {
                System.out.printf("$%14.2f", matrizVentas[i][j]);
            }
            System.out.println();
        }
        System.out.println("============================================================");
    }

    public static void main(String[] args) {
        VentasDepartamentos gestor = new VentasDepartamentos();
        Scanner scanner = new Scanner(System.in);

        // Datos iniciales de demostración
        gestor.insertarVenta("Enero", "Ropa", 15000.50);
        gestor.insertarVenta("Enero", "Deportes", 23000.00);
        gestor.insertarVenta("Febrero", "Juguetería", 18500.25);
        gestor.insertarVenta("Diciembre", "Juguetería", 45000.00);

        while (true) {
            System.out.println("\n--- MENÚ DE GESTIÓN DE VENTAS (JAVA) ---");
            System.out.println("1. Insertar / Actualizar venta");
            System.out.println("2. Buscar venta");
            System.out.println("3. Eliminar venta");
            System.out.println("4. Mostrar tabla completa de ventas");
            System.out.println("5. Salir");
            System.out.print("Selecciona una opción (1-5): ");

            String opcion = scanner.nextLine().trim();

            if (opcion.equals("1")) {
                System.out.print("Ingresa el mes (Nombre o número 1-12): ");
                String mes = scanner.nextLine();
                System.out.print("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ");
                String dep = scanner.nextLine();
                System.out.print("Ingresa el monto de la venta: ");
                try {
                    double monto = Double.parseDouble(scanner.nextLine());
                    gestor.insertarVenta(mes, dep, monto);
                } catch (NumberFormatException e) {
                    System.out.println("Error: Ingresa un monto válido.");
                }
            } else if (opcion.equals("2")) {
                System.out.print("Ingresa el mes (Nombre o número 1-12): ");
                String mes = scanner.nextLine();
                System.out.print("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ");
                String dep = scanner.nextLine();
                gestor.buscarVenta(mes, dep);
            } else if (opcion.equals("3")) {
                System.out.print("Ingresa el mes (Nombre o número 1-12): ");
                String mes = scanner.nextLine();
                System.out.print("Ingresa el departamento (Ropa, Deportes, Juguetería o 1-3): ");
                String dep = scanner.nextLine();
                gestor.eliminarVenta(mes, dep);
            } else if (opcion.equals("4")) {
                gestor.mostrarTabla();
            } else if (opcion.equals("5")) {
                System.out.println("Saliendo del programa Java...");
                break;
            } else {
                System.out.println("Opción no válida. Intenta de nuevo.");
            }
        }
        scanner.close();
    }
}
