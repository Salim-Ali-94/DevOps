import styles from "./styles.module.css";
import Image from "next/image";
import { useState } from "react";


export default function Modal({ setVisible }) {

    const [todo, setTodo] = useState("");

    async function saveTodo() {

        await fetch("/api/server",
                    { method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({ item: todo, 
                                             completed: false }) });

        setVisible(false);

    }

    return (

        <div className={styles.overlay}>

            <form className={styles.modal}
                  onSubmit={(event) => event.preventDefault()}>

                <div className={styles.xButton}>

                    <div className={styles.circle}
                         onClick={() => setVisible(false)}>

                        <Image src="/assets/icons/x.png"
                               width={20}
                               height={20}
                               alt="close-icon" />

                    </div>

                </div>

                <label className={styles.headingText}>Add a new item to your checklist</label>

                <input className={styles.inputField}
                        placeholder="New item"
                        onChange={(event) => setTodo(event.target.value)}
                        value={todo}
                        type="text"/>

                <button className={styles.submitButton}
                        onClick={saveTodo}>Submit</button>

            </form>

        </div>

    );

}
