// lsp_good_bad.ts

// BAD Example (violates LSP)
class Rectangle {
  protected _width: number;
  protected _height: number;

  constructor(width: number, height: number) {
    this._width = width;
    this._height = height;
  }

  get width(): number { return this._width; }
  set width(value: number) { this._width = value; }

  get height(): number { return this._height; }
  set height(value: number) { this._height = value; }

  area(): number { return this._width * this._height; }
}

class Square extends Rectangle {
  constructor(size: number) {
    super(size, size);
  }

  // Violates LSP: Square changes the behavior of width/height setters
  // A Square should not allow its width and height to be set independently.
  set width(value: number) {
    this._width = value;
    this._height = value;
  }

  set height(value: number) {
    this._width = value;
    this._height = value;
  }
}

function printArea(rect: Rectangle): void {
  rect.width = 5;
  rect.height = 4;
  console.log(`Expected area: 20, Actual area: ${rect.area()}`);
}

const rect = new Rectangle(2, 3);
printArea(rect); // Expected: 20, Actual: 20

const square = new Square(3);
printArea(square); // Expected: 20, Actual: 16 (because setting width=5 also sets height=5, then setting height=4 sets width=4)

// GOOD Example (adheres to LSP)

interface ShapeWithArea {
  area(): number;
}

class RectangleLSP implements ShapeWithArea {
  constructor(public width: number, public height: number) {}
  area(): number { return this.width * this.height; }
}

class SquareLSP implements ShapeWithArea {
  constructor(public side: number) {}
  area(): number { return this.side * this.side; }
}

// Function that operates on the abstraction ShapeWithArea
function calculateAndPrintArea(shape: ShapeWithArea): void {
  console.log(`Calculated area: ${shape.area()}`);
}

const rectLSP = new RectangleLSP(2, 3);
const squareLSP = new SquareLSP(3);

calculateAndPrintArea(rectLSP);   // Output: Calculated area: 6
calculateAndPrintArea(squareLSP); // Output: Calculated area: 9
