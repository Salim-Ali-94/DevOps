
export default async function handler(request, response) {

  try {

    const data = request.body;
    await fetch(process.env.API_ENTRYPOINT)
    const result = await fetch(process.env.STORE_TODO_ENDPOINT,
                               { method: "POST",
                                 headers: { "Content-Type": "application/json" },
                                 body: JSON.stringify(data) });

    if (result.ok) {

      response.status(200).end();

    } else {

      throw new Error("Failed to save todo item");

    }

  } catch (error) {

    console.error("Server error:", error);
    response.status(500).json({ error: "An error occured while fetching your data" });

  }

}
