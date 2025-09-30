import { NextResponse } from "next/server";

export async function POST(
  request: Request,
  { params }: { params: { routerId: string } }
) {
  const { routerId } = params;
  const body = await request.json();

  console.log(`Webhook received for router ${routerId}:`, body);

  return NextResponse.json({ status: "received" });
}

