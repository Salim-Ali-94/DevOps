mod utility;


fn main() {

    let msg = "Lift off".to_string();
    let aes_standard = 192;
    let (encrypted_msg, key, encrypted_doc, hex_key) = utility::scrambleDocument(msg.clone(), aes_standard);
    println!("\n\nthe aes key is = {} / {}-bits\n\n", key, key.len());
    println!("stacked hex key is = {:?}\n\n", hex_key);
    println!("original message is = '{}'\n\n", msg.clone());
    println!("for {}-bit aes standard:\n", aes_standard);
    println!("encrypted message is = {:?}\n\n", encrypted_msg);
    println!("encrypted message matrix = {:?}\n\n", encrypted_doc);

}
