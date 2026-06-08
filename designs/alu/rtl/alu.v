// Simple ALU for flow automation practice.
module alu (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire [2:0] op,
    output reg  [7:0] y,
    output wire       zero
);

assign zero = (y == 8'b0);

always @(*) begin
    case (op)
        3'b000: y = a + b;
        3'b001: y = a - b;
        3'b010: y = a & b;
        3'b011: y = a | b;
        3'b100: y = a ^ b;
        3'b101: y = b << 1;
        3'b110: y = b >> 1;
        default: y = 8'b0;
    endcase
end

endmodule

