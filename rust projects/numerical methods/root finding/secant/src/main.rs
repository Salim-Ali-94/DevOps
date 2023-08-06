mod utility;


fn main() {

    let f = |x: f64| {

        3.0*x.powf(3.0) - x - 1.0
    };

    let w: [f64; 2] = [-100.0, 100.0];
    println!("f(4.3) = {}", f(4.3));
    let int = utility::findInterval(f, w);
    println!("ints --> {:?}", int);

}
