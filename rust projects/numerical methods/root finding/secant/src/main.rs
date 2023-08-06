

fn main() {

    let f = |x: f64| {

        3.0*x.powf(3.0) - x - 1.0
    };

    println!("f(4.3) = {}", f(4.3));

}
