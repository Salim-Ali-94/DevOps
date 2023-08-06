mod utility;


fn main() {

    let f = |x: f64| {

        x.powf(3.0) - x.powf(2.0) - 2.0*x + 1.0
    };

    let domain: [f64; 2] = [-100.0, 100.0];
    let tolerance = 1e-3;
    let (solutions, epsilon, cycles) = utility::secant(f, domain, tolerance);
    println!("\nFound {} root(s) with a precision of {} in {} iterations inside the window; from x = {} to x = {} for the given function\n", solutions.len(), epsilon, cycles, domain[0], domain[1]);

    for root in solutions.iter() {

        println!("\nf({}) = {}", root, f(*root));

    }

}
