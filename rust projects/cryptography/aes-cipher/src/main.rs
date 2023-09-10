mod utility;


fn main() {

    // let msg = "Lift off".to_string();
    // let aes_standard = 128;
    let msg = "Let none ignorant of calculus enter here.".to_string();
    // let aes_standard = 192;
    let aes_standard = 256;
    let (encrypted_msg, key) = utility::scrambleDocument(msg.clone(), aes_standard);
    println!("\n\nthe aes key is = {} / {}-bits\n", key, key.len());
    println!("original message is = '{}'\n", msg.clone());
    println!("for {}-bit aes standard:\n", aes_standard);
    println!("encrypted message is = {}\n", encrypted_msg);
    let text = utility::extractDocument(encrypted_msg, key);
    println!("message = {}\n\n", text);

}
