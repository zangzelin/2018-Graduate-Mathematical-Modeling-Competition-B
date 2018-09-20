%1.2
xinzao = [10^0.93, 10^1.33, 10^1.57]; %信噪比
k = 2 * pi * 6.62606896 * (10^(-10)) * 193.1 * 50; %噪声系数
G = [(2)^(80/15), (2)^(100/15)]; %增益
Pn = k * (4 - 1 ./ G) .* G; %噪声

for j = 1:2

    for i = 1:3
        n(i, j) = floor(1 / xinzao(i) / Pn(j)); %计算N跨
    end

end

%2.3
A = xlsread("a.xlsx"); %导入数据，分别为距离，人口，人均收入，容量

for i = 1:4%求出每一列的最大最小值
    amin(i) = min(A(:, i));
    amax(i) = max(A(:, i));
end

amax(1) = 3000; %设定距离上限
amax(2) = 50; %设定人口上限
amax(3) = 50000; %设定收入上限
amin(2) = 15; %设定人口下限

for i = 1:1%距离标准化

    for j = 1:144

        if A(j, i) > 3000
            B(j, i) = 0;
        else
            B(j, i) = (amax(i) - A(j, i)) / (amax(i) - amin(i)); %负向指标
        end

    end

end

for i = 3:3%人均收入标准化

    for j = 1:144

        if A(j, i) > 50000
            B(j, i) = 1;
        else
            B(j, i) = (A(j, i) - amin(i)) / (amax(i) - amin(i)); %正向指标
        end

    end

end

for i = 2:2%人口标准化

    for j = 1:144

        if A(j, i) > 50
            B(j, i) = 1;
        elseif A(j, i) < 15
            B(j, i) = 0;
        else
            B(j, i) = (A(j, i) - amin(i)) / (amax(i) - amin(i)); %正向指标
        end

    end

end

for i = 4:4
    B(:, i) = (A(:, i) - amin(i)) / (amax(i) - amin(i)); %正向指标
end

for i = 1:4%归一化处理
    a(i) = sum(B(:, i));
end

for i = 1:4
    C(:, i) = B(:, i) / a(i);
end

g = zeros(1, 4);

for i = 1:4

    for j = 1:144

        if C(j, i) == 0%如果c（i，j）=0，plnp为0
            f = 0;
        elseif C(j, i) ~= 0;
            f = log(C(j, i)) .* C(j, i);
        end

        g(i) = g(i) + f;
    end

end

h = -g / log(144); %信息熵
G = 1 - h;
H = G / sum(G); %权重
