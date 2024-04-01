import java.util.ArrayList;
import java.util.List;

interface MathOperation {
    int operate(int a, int b);
}

class Addition implements MathOperation {
    public int operate(int a, int b) {
        return a + b;
    }
}
class Subtraction implements MathOperation {
    public int operate(int a, int b) {
        return a - b;
    }
}

class Calculator {
    public int executeOperation(MathOperation operation, int a, int b) {
        return operation.operate(a, b);
    }
}

class ComplexCalculator extends Calculator {
    public List<Integer> performSeriesOperations(int[] numbers, MathOperation operation) {
        List<Integer> results = new ArrayList<>();
        for (int i = 0; i < numbers.length - 1; i++) {
            results.add(operation.operate(numbers[i], numbers[i + 1]));
        }
        return results;
    }
}

class AdvancedMath {
    public static void main(String[] args) {
        Calculator simpleCalc = new Calculator();
        ComplexCalculator complexCalc = new ComplexCalculator();

        Addition addition = new Addition();
        Subtraction subtraction = new Subtraction();

        System.out.println("Simple Addition: " + simpleCalc.executeOperation(addition, 5, 3));
        System.out.println("Simple Subtraction: " + simpleCalc.executeOperation(subtraction, 5, 3));

        int[] numbers = {1, 2, 3, 4, 5};
        List<Integer> additionResults = complexCalc.performSeriesOperations(numbers, addition);
        List<Integer> subtractionResults = complexCalc.performSeriesOperations(numbers, subtraction);

        System.out.println("Series Addition: " + additionResults);
        System.out.println("Series Subtraction: " + subtractionResults);
    }
}
